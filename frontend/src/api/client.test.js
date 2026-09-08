import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  ApiError,
  api,
  clearToken,
  getToken,
  request,
  setToken,
  setUnauthorizedHandler,
} from "./client";
import { TOKEN_STORAGE_KEY } from "../config/env";

/** Build a Response-like object for the mocked fetch. */
function jsonResponse(body, { status = 200 } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

function emptyResponse({ status = 200 } = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => {
      throw new Error("no body");
    },
    text: async () => "",
  };
}

describe("api client", () => {
  beforeEach(() => {
    setUnauthorizedHandler(null);
  });

  describe("token storage", () => {
    it("round-trips the token", () => {
      expect(getToken()).toBeNull();

      setToken("abc123");
      expect(getToken()).toBe("abc123");
      expect(localStorage.getItem(TOKEN_STORAGE_KEY)).toBe("abc123");

      clearToken();
      expect(getToken()).toBeNull();
    });
  });

  describe("request", () => {
    it("prefixes the base URL and attaches the bearer token", async () => {
      setToken("my-token");
      globalThis.fetch.mockResolvedValue(jsonResponse({ ok: true }));

      await request("/conversations/");

      const [url, options] = globalThis.fetch.mock.calls[0];

      expect(url).toBe("http://localhost:8000/conversations/");
      expect(options.headers.Authorization).toBe("Bearer my-token");
    });

    it("omits the Authorization header when auth is disabled", async () => {
      setToken("my-token");
      globalThis.fetch.mockResolvedValue(jsonResponse({}));

      await request("/auth/login", { auth: false });

      const [, options] = globalThis.fetch.mock.calls[0];
      expect(options.headers.Authorization).toBeUndefined();
    });

    it("sends objects as JSON", async () => {
      globalThis.fetch.mockResolvedValue(jsonResponse({}));

      await api.post("/chat", { question: "hi" });

      const [, options] = globalThis.fetch.mock.calls[0];

      expect(options.headers["Content-Type"]).toBe("application/json");
      expect(options.body).toBe(JSON.stringify({ question: "hi" }));
    });

    it("lets the browser set Content-Type for FormData", async () => {
      globalThis.fetch.mockResolvedValue(jsonResponse({}));

      const form = new FormData();
      form.append("file", "x");

      await api.post("/upload/", form);

      const [, options] = globalThis.fetch.mock.calls[0];

      // A manual multipart Content-Type would omit the boundary and break
      // the upload.
      expect(options.headers["Content-Type"]).toBeUndefined();
      expect(options.body).toBe(form);
    });

    it("surfaces the backend's detail message", async () => {
      globalThis.fetch.mockResolvedValue(
        jsonResponse({ detail: "Email already registered." }, { status: 400 })
      );

      await expect(
        api.post("/auth/register", {}, { auth: false })
      ).rejects.toThrow("Email already registered.");
    });

    it("falls back to the supplied message when there is no detail", async () => {
      globalThis.fetch.mockResolvedValue(emptyResponse({ status: 500 }));

      await expect(
        request("/conversations/", { errorMessage: "Unable to load." })
      ).rejects.toThrow("Unable to load.");
    });

    it("throws an ApiError carrying the status", async () => {
      globalThis.fetch.mockResolvedValue(
        jsonResponse({ detail: "Nope." }, { status: 404 })
      );

      await expect(request("/missing")).rejects.toMatchObject({
        name: "ApiError",
        status: 404,
      });

      await expect(request("/missing")).rejects.toBeInstanceOf(ApiError);
    });

    it("returns null for an empty body", async () => {
      globalThis.fetch.mockResolvedValue(emptyResponse());

      await expect(request("/conversations/")).resolves.toBeNull();
    });
  });

  describe("401 handling", () => {
    it("clears the token and notifies the handler", async () => {
      setToken("expired-token");

      const onUnauthorized = vi.fn();
      setUnauthorizedHandler(onUnauthorized);

      globalThis.fetch.mockResolvedValue(
        jsonResponse({ detail: "Could not validate credentials" }, { status: 401 })
      );

      await expect(request("/conversations/")).rejects.toThrow(
        "Could not validate credentials"
      );

      // Without this the user sits on a page that can never load.
      expect(getToken()).toBeNull();
      expect(onUnauthorized).toHaveBeenCalledTimes(1);
    });

    it("does not trigger logout for unauthenticated requests", async () => {
      const onUnauthorized = vi.fn();
      setUnauthorizedHandler(onUnauthorized);

      globalThis.fetch.mockResolvedValue(
        jsonResponse({ detail: "Invalid email or password." }, { status: 401 })
      );

      await expect(
        api.post("/auth/login", {}, { auth: false })
      ).rejects.toThrow("Invalid email or password.");

      // A failed login is not an expired session.
      expect(onUnauthorized).not.toHaveBeenCalled();
    });
  });
});
