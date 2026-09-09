import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import NotFound from "./NotFound";
import { AuthProvider } from "../context/AuthContext";
import { setToken } from "../api/client";

function renderNotFound() {
  return render(
    <MemoryRouter initialEntries={["/no-such-page"]}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<p>Login page</p>} />
          <Route path="/workspace" element={<p>Workspace page</p>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>
  );
}

describe("NotFound", () => {
  it("shows a 404 instead of silently redirecting", async () => {
    renderNotFound();

    expect(await screen.findByText("Page not found")).toBeInTheDocument();
    // The old wildcard route sent every unknown URL to login.
    expect(screen.queryByText("Login page")).not.toBeInTheDocument();
  });

  it("offers sign-in to a signed-out visitor", async () => {
    const user = userEvent.setup();

    renderNotFound();

    await user.click(
      await screen.findByRole("button", { name: /go to sign in/i })
    );

    expect(await screen.findByText("Login page")).toBeInTheDocument();
  });

  it("offers the workspace to a signed-in user rather than logging them out", async () => {
    setToken("valid-token");

    globalThis.fetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: 1, username: "ruchika", email: "r@example.com" }),
      text: async () => JSON.stringify({ id: 1 }),
    });

    const user = userEvent.setup();

    renderNotFound();

    await user.click(
      await screen.findByRole("button", { name: /back to workspace/i })
    );

    expect(await screen.findByText("Workspace page")).toBeInTheDocument();
  });
});
