/**
 * Navigation definitions.
 *
 * Kept out of Sidebar.jsx so that file exports only a component, which is
 * what React Fast Refresh requires.
 */

/** The four workspace destinations, shown on most pages. */
export const WORKSPACE_NAV = [
  { to: "/workspace", icon: "⌂", label: "Overview" },
  { to: "/knowledge", icon: "✦", label: "Knowledge" },
  { to: "/agents", icon: "◇", label: "Agents" },
  { to: "/tools", icon: "⌁", label: "Connected tools" },
];

/** Settings shows a shorter list, pinned to the bottom of the rail. */
export const SETTINGS_NAV = [
  { to: "/workspace", icon: "⌂", label: "Workspace" },
  { to: "/settings", icon: "⚙", label: "Settings" },
];

export const BACK_TO_WORKSPACE = {
  to: "/workspace",
  icon: "←",
  label: "Back to workspace",
};

export const NEW_CONVERSATION = {
  to: "/chat",
  icon: "+",
  label: "New conversation",
};
