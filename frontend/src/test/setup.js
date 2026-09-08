import "@testing-library/jest-dom/vitest";

import { afterEach, beforeEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => {
  cleanup();
});

beforeEach(() => {
  // Each test starts with empty storage so a token left behind by one test
  // cannot silently authenticate the next.
  localStorage.clear();

  // Nothing should reach the network. Individual tests replace this.
  vi.spyOn(globalThis, "fetch").mockRejectedValue(
    new Error("Unexpected network call in test. Mock fetch explicitly.")
  );
});
