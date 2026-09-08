import { describe, expect, it } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./ProtectedRoute";
import { AuthProvider } from "../context/AuthContext";
import { setToken } from "../api/client";

function renderApp(initialPath) {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<p>Login page</p>} />
          <Route
            path="/chat"
            element={
              <ProtectedRoute>
                <p>Chat page</p>
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </MemoryRouter>
  );
}

describe("ProtectedRoute", () => {
  it("redirects an unauthenticated visitor to login", async () => {
    renderApp("/chat");

    expect(await screen.findByText("Login page")).toBeInTheDocument();
    expect(screen.queryByText("Chat page")).not.toBeInTheDocument();
  });

  it("renders the page when a token is present", async () => {
    setToken("valid-token");

    // AuthProvider loads the profile on mount.
    globalThis.fetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: 1, username: "ruchika", email: "r@example.com" }),
      text: async () => JSON.stringify({ id: 1, username: "ruchika" }),
    });

    renderApp("/chat");

    expect(await screen.findByText("Chat page")).toBeInTheDocument();
    expect(screen.queryByText("Login page")).not.toBeInTheDocument();
  });

  it("sends the user back to login when the token is rejected", async () => {
    setToken("expired-token");

    globalThis.fetch.mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ detail: "Could not validate credentials" }),
      text: async () => "",
    });

    renderApp("/chat");

    // The 401 handler clears auth state, so the guard re-evaluates.
    await waitFor(() => {
      expect(screen.getByText("Login page")).toBeInTheDocument();
    });
  });
});
