import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import ResetPassword from "./ResetPassword";

function renderPage(search = "?token=reset-token-123") {
  return render(
    <MemoryRouter initialEntries={[`/reset-password${search}`]}>
      <Routes>
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/login" element={<p>Login page</p>} />
        <Route path="/forgot-password" element={<p>Forgot page</p>} />
      </Routes>
    </MemoryRouter>
  );
}

function mockSuccess() {
  globalThis.fetch.mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => ({ message: "Your password has been reset." }),
    text: async () => JSON.stringify({ message: "ok" }),
  });
}

describe("ResetPassword", () => {
  it("refuses a link with no token", () => {
    renderPage("");

    expect(screen.getByText(/invalid reset link/i)).toBeInTheDocument();
    expect(
      screen.queryByLabelText("New password")
    ).not.toBeInTheDocument();
  });

  it("sends the token and the new password", async () => {
    const user = userEvent.setup();
    mockSuccess();

    renderPage();

    await user.type(screen.getByLabelText("New password"), "a-good-password");
    await user.type(
      screen.getByLabelText("Confirm new password"),
      "a-good-password"
    );
    await user.click(screen.getByRole("button", { name: /update password/i }));

    expect(await screen.findByText(/password updated/i)).toBeInTheDocument();

    const [url, options] = globalThis.fetch.mock.calls[0];

    expect(url).toBe("http://localhost:8000/auth/reset-password");
    expect(JSON.parse(options.body)).toEqual({
      token: "reset-token-123",
      new_password: "a-good-password",
    });
  });

  it("rejects mismatched passwords without calling the API", async () => {
    const user = userEvent.setup();

    renderPage();

    await user.type(screen.getByLabelText("New password"), "a-good-password");
    await user.type(
      screen.getByLabelText("Confirm new password"),
      "a-different-one"
    );
    await user.click(screen.getByRole("button", { name: /update password/i }));

    expect(
      await screen.findByText("Passwords do not match.")
    ).toBeInTheDocument();
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  it("surfaces an expired or already-used link", async () => {
    const user = userEvent.setup();

    globalThis.fetch.mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({
        detail: "This password reset link is invalid or has expired.",
      }),
      text: async () => "",
    });

    renderPage();

    await user.type(screen.getByLabelText("New password"), "a-good-password");
    await user.type(
      screen.getByLabelText("Confirm new password"),
      "a-good-password"
    );
    await user.click(screen.getByRole("button", { name: /update password/i }));

    expect(
      await screen.findByText(
        "This password reset link is invalid or has expired."
      )
    ).toBeInTheDocument();
    expect(screen.queryByText(/password updated/i)).not.toBeInTheDocument();
  });
});
