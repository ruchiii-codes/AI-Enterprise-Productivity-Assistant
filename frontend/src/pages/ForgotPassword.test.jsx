import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import ForgotPassword from "./ForgotPassword";

function renderPage() {
  return render(
    <MemoryRouter initialEntries={["/forgot-password"]}>
      <Routes>
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/login" element={<p>Login page</p>} />
      </Routes>
    </MemoryRouter>
  );
}

function mockAccepted() {
  globalThis.fetch.mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => ({ message: "If that email address has an account..." }),
    text: async () =>
      JSON.stringify({ message: "If that email address has an account..." }),
  });
}

describe("ForgotPassword", () => {
  it("posts the email to the forgot-password endpoint", async () => {
    const user = userEvent.setup();
    mockAccepted();

    renderPage();

    await user.type(screen.getByLabelText("Email"), "r@example.com");
    await user.click(screen.getByRole("button", { name: /send reset link/i }));

    await screen.findByText(/reset link sent/i);

    const [url, options] = globalThis.fetch.mock.calls[0];

    expect(url).toBe("http://localhost:8000/auth/forgot-password");
    expect(options.method).toBe("POST");
    expect(JSON.parse(options.body)).toEqual({ email: "r@example.com" });
    // No token is attached: the user is not signed in.
    expect(options.headers.Authorization).toBeUndefined();
  });

  it("does not confirm whether the account exists", async () => {
    const user = userEvent.setup();
    mockAccepted();

    renderPage();

    await user.type(screen.getByLabelText("Email"), "nobody@example.com");
    await user.click(screen.getByRole("button", { name: /send reset link/i }));

    // Wording must stay conditional, or the page becomes an account oracle.
    expect(await screen.findByText(/if /i)).toBeInTheDocument();
    expect(screen.getByText(/has a WorkMind/i)).toBeInTheDocument();
  });

  it("shows an error when the request fails", async () => {
    const user = userEvent.setup();

    globalThis.fetch.mockResolvedValue({
      ok: false,
      status: 429,
      json: async () => ({ detail: "Too many requests." }),
      text: async () => "",
    });

    renderPage();

    await user.type(screen.getByLabelText("Email"), "r@example.com");
    await user.click(screen.getByRole("button", { name: /send reset link/i }));

    expect(await screen.findByText("Too many requests.")).toBeInTheDocument();
    expect(screen.queryByText(/reset link sent/i)).not.toBeInTheDocument();
  });
});
