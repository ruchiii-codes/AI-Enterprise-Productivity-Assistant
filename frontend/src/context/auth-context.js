import { createContext } from "react";

/**
 * Kept in its own module so AuthContext.jsx exports only a component, which
 * is what React Fast Refresh requires.
 */
export const AuthContext = createContext(null);
