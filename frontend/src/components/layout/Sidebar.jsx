import { Link, useLocation } from "react-router-dom";

import Brand from "../ui/Brand";
import { BACK_TO_WORKSPACE, WORKSPACE_NAV } from "./nav-items";

/**
 * The workspace navigation rail.
 *
 * This markup was previously repeated inline in five pages. The active item
 * is derived from the current route rather than hardcoded per page, so a page
 * can no longer disagree with the URL about where the user is.
 */
export function Sidebar({
  topAction = BACK_TO_WORKSPACE,
  items = WORKSPACE_NAV,
  label = "WORKSPACE",
  placement = "section",
}) {
  const { pathname } = useLocation();

  const nav = items.map((item) => (
    <Link
      key={item.to}
      to={item.to}
      className={`workspace-nav ${pathname === item.to ? "active" : ""}`}
    >
      <span>{item.icon}</span>
      {item.label}
    </Link>
  ));

  return (
    <aside className="workspace-sidebar">
      <div className="sidebar-top">
        <Brand compact />

        <Link to={topAction.to} className="new-chat-button">
          <span>{topAction.icon}</span>
          <span>{topAction.label}</span>
        </Link>

        {placement === "section" && (
          <div className="sidebar-section">
            <div className="sidebar-label">{label}</div>
            {nav}
          </div>
        )}
      </div>

      {placement === "bottom" && (
        <div className="sidebar-bottom">{nav}</div>
      )}
    </aside>
  );
}

export default Sidebar;
