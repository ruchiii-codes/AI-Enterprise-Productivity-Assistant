import { describe, expect, it } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import Login from "./Login";
import { AuthProvider } from "../context/AuthContext";
import { getToken } from "../api/client";

function renderLogin(initialEntry = "/login") {
  return render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/workspace" element={<p>Workspace page</p>} />
          <Route path="/chat" element={<p>Chat page</p>} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>
  );
}

function mockLoginSuccess(token = "issued-token") {
  globalThis.fetch.mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => ({ access_token: token, token_type: "bearer" }),
    text: async () => JSON.stringify({ access_token: token }),
  });
}

describe("Login", () => {
  it("renders the sign-in form", () => {
    renderLogin();

    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /sign in/i })
    ).toBeInTheDocument();
  });

  it("submits credentials as form encoding and stores the token", async () => {
    const user = userEvent.setup();
    mockLoginSuccess();

    renderLogin();

    await user.type(screen.getByLabelText("Email"), "r@example.com");
    await user.type(screen.getByLabelText("Password"), "secret123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText("Workspace page")).toBeInTheDocument();
    });

    const [url, options] = globalThis.fetch.mock.calls[0];

    expect(url).toBe("http://localhost:8000/auth/login");
    expect(options.method).toBe("POST");
    // The backend uses OAuth2PasswordRequestForm, so the email goes in
    // "username" and the body must be form encoded, not JSON.
    expect(options.headers["Content-Type"]).toBe(
      "application/x-www-form-urlencoded"
    );
    expect(options.body.get("username")).toBe("r@example.com");
    expect(options.body.get("password")).toBe("secret123");

    expect(getToken()).toBe("issued-token");
  });

  it("shows the backend's message and stays put when login fails", async () => {
    const user = userEvent.setup();

    globalThis.fetch.mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: "Invalid email or password." }),
      text: async () => "",
    });

    renderLogin();

    await user.type(screen.getByLabelText("Email"), "r@example.com");
    await user.type(screen.getByLabelText("Password"), "wrong");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(
      await screen.findByText("Invalid email or password.")
    ).toBeInTheDocument();

    expect(screen.queryByText("Workspace page")).not.toBeInTheDocument();
    expect(getToken()).toBeNull();
  });

  it("returns the user to the page they were sent away from", async () => {
    const user = userEvent.setup();
    mockLoginSuccess();

    render(
      <MemoryRouter
        initialEntries={[
          { pathname: "/login", state: { from: { pathname: "/chat" } } },
        ]}
      >
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/workspace" element={<p>Workspace page</p>} />
            <Route path="/chat" element={<p>Chat page</p>} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    await user.type(screen.getByLabelText("Email"), "r@example.com");
    await user.type(screen.getByLabelText("Password"), "secret123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText("Chat page")).toBeInTheDocument();
    });
  });
});
