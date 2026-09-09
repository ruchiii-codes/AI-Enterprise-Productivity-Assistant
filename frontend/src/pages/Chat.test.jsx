/**
 * Behavioural tests for the chat page.
 *
 * Written against the original 985-line Chat.jsx and kept unchanged through
 * the component split, so that a passing run after the refactor is evidence
 * the split altered no behaviour. They exercise what the user does, never
 * internal structure.
 */

import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";

import Chat from "./Chat";
import { AuthProvider } from "../context/AuthContext";
import { setToken } from "../api/client";
import { CONVERSATION_STORAGE_KEY } from "../config/env";

const CONVERSATIONS = [
  { id: 1, title: "Hybrid search", message_count: 2, is_pinned: false, pinned_at: null },
  { id: 2, title: "Quarterly report", message_count: 4, is_pinned: false, pinned_at: null },
];

const MESSAGES = [
  { role: "user", content: "What is hybrid search?" },
  { role: "assistant", content: "It combines semantic and keyword retrieval." },
];

/**
 * Route fetch by URL so tests describe server behaviour rather than call
 * order, which the refactor is free to change.
 */
function mockApi(overrides = {}) {
  const handlers = {
    "GET /conversations/": () => CONVERSATIONS,
    "GET /messages/": () => MESSAGES,
    "GET /documents/": () => [],
    "GET /auth/me": () => ({ id: 1, username: "ruchika", email: "r@example.com" }),
    "POST /conversations/": () => ({ id: 3, title: "New Conversation", message_count: 0 }),
    "POST /chat": () => ({ answer: "Here is your answer.", sources: [] }),
    "POST /upload/": () => ({ message: "Uploaded." }),
    "DELETE /conversations/": () => ({ message: "Deleted." }),
    ...overrides,
  };

  globalThis.fetch.mockImplementation(async (url, options = {}) => {
    const method = options.method || "GET";
    const path = String(url).replace("http://localhost:8000", "");

    const key = Object.keys(handlers).find((candidate) => {
      const [handlerMethod, handlerPath] = candidate.split(" ");
      return method === handlerMethod && path.startsWith(handlerPath);
    });

    if (!key) {
      return {
        ok: false,
        status: 404,
        json: async () => ({ detail: `Unhandled ${method} ${path}` }),
        text: async () => "",
      };
    }

    const body = handlers[key]();

    if (body?.__error) {
      return {
        ok: false,
        status: body.status,
        json: async () => ({ detail: body.detail }),
        text: async () => "",
      };
    }

    return {
      ok: true,
      status: 200,
      json: async () => body,
      text: async () => JSON.stringify(body),
    };
  });
}

function renderChat() {
  return render(
    <MemoryRouter initialEntries={["/chat"]}>
      <AuthProvider>
        <Chat />
      </AuthProvider>
    </MemoryRouter>
  );
}

/** Requests matching a method and path prefix. */
function callsTo(method, pathPrefix) {
  return globalThis.fetch.mock.calls.filter(([url, options = {}]) => {
    const callMethod = options.method || "GET";
    const path = String(url).replace("http://localhost:8000", "");
    return callMethod === method && path.startsWith(pathPrefix);
  });
}

describe("Chat", () => {
  beforeEach(() => {
    setToken("valid-token");
    localStorage.setItem(CONVERSATION_STORAGE_KEY, "1");
  });

  it("lists the conversations that have messages", async () => {
    mockApi();

    renderChat();

    expect(await screen.findByText("Hybrid search")).toBeInTheDocument();
    expect(screen.getByText("Quarterly report")).toBeInTheDocument();
  });

  it("hides conversations with no messages", async () => {
    mockApi({
      "GET /conversations/": () => [
        ...CONVERSATIONS,
        { id: 9, title: "Empty one", message_count: 0, is_pinned: false },
      ],
    });

    renderChat();

    await screen.findByText("Hybrid search");
    expect(screen.queryByText("Empty one")).not.toBeInTheDocument();
  });

  it("restores the conversation saved in storage and shows its messages", async () => {
    mockApi();

    renderChat();

    expect(
      await screen.findByText("It combines semantic and keyword retrieval.")
    ).toBeInTheDocument();

    expect(callsTo("GET", "/messages/1").length).toBeGreaterThan(0);
  });

  it("loads a conversation when it is selected", async () => {
    const user = userEvent.setup();
    mockApi();

    renderChat();

    await user.click(await screen.findByText("Quarterly report"));

    await waitFor(() => {
      expect(callsTo("GET", "/messages/2").length).toBeGreaterThan(0);
    });

    expect(localStorage.getItem(CONVERSATION_STORAGE_KEY)).toBe("2");
  });

  it("sends a message and shows the reply", async () => {
    const user = userEvent.setup();
    mockApi();

    renderChat();

    await screen.findByText("Hybrid search");

    const composer = screen.getByPlaceholderText("Ask WorkMind anything...");

    await user.type(composer, "Summarise this");
    await user.click(screen.getByRole("button", { name: "↑" }));

    expect(await screen.findByText("Here is your answer.")).toBeInTheDocument();

    const [, options] = callsTo("POST", "/chat")[0];
    expect(JSON.parse(options.body)).toEqual({
      question: "Summarise this",
      conversation_id: 1,
    });
  });

  it("will not send an empty message", async () => {
    mockApi();

    renderChat();

    await screen.findByText("Hybrid search");

    expect(screen.getByRole("button", { name: "↑" })).toBeDisabled();
    expect(callsTo("POST", "/chat")).toHaveLength(0);
  });

  it("surfaces an error from the chat endpoint", async () => {
    const user = userEvent.setup();
    mockApi({
      "POST /chat": () => ({
        __error: true,
        status: 503,
        detail: "The AI service is currently unavailable.",
      }),
    });

    renderChat();

    await screen.findByText("Hybrid search");

    await user.type(
      screen.getByPlaceholderText("Ask WorkMind anything..."),
      "Hello"
    );
    await user.click(screen.getByRole("button", { name: "↑" }));

    expect(
      await screen.findByText("The AI service is currently unavailable.")
    ).toBeInTheDocument();
  });

  it("creates a conversation from the new-conversation control", async () => {
    const user = userEvent.setup();
    mockApi();

    renderChat();

    await screen.findByText("Hybrid search");

    const newButton = screen.getByRole("button", { name: /new conversation/i });
    await user.click(newButton);

    await waitFor(() => {
      expect(callsTo("POST", "/conversations/").length).toBe(1);
    });
  });

  it("deletes a conversation after confirmation", async () => {
    const user = userEvent.setup();
    mockApi();

    vi.spyOn(window, "confirm").mockReturnValue(true);

    renderChat();

    const item = (await screen.findByText("Quarterly report")).closest(
      ".conversation"
    );

    // The row menu is revealed on the conversation itself.
    const menuButton = within(item).getByRole("button", { name: "⋯" });
    await user.click(menuButton);

    await user.click(screen.getByRole("button", { name: /delete/i }));

    await waitFor(() => {
      expect(callsTo("DELETE", "/conversations/2").length).toBe(1);
    });

    await waitFor(() => {
      expect(screen.queryByText("Quarterly report")).not.toBeInTheDocument();
    });
  });

  it("searches conversations", async () => {
    const user = userEvent.setup();
    mockApi({
      "GET /conversations/search": () => [CONVERSATIONS[1]],
    });

    renderChat();

    await screen.findByText("Hybrid search");

    // The trigger is labelled by its title attribute, not visible text.
    await user.click(screen.getByTitle("Search conversations"));

    const input = await screen.findByPlaceholderText(
      "Search your conversations..."
    );

    await user.type(input, "quarterly");

    await waitFor(() => {
      expect(callsTo("GET", "/conversations/search").length).toBeGreaterThan(0);
    });
  });

  it("rejects a non-PDF upload without calling the API", async () => {
    mockApi();

    renderChat();

    await screen.findByText("Hybrid search");

    const input = document.querySelector('input[type="file"]');
    const notAPdf = new File(["x"], "notes.txt", { type: "text/plain" });

    // The input is hidden, so userEvent.upload will not drive it.
    fireEvent.change(input, { target: { files: [notAPdf] } });

    expect(await screen.findByText(/please upload a pdf/i)).toBeInTheDocument();
    expect(callsTo("POST", "/upload/")).toHaveLength(0);
  });
});
