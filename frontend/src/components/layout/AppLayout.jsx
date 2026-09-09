import ProfileMenu from "./ProfileMenu";
import Sidebar from "./Sidebar";

/**
 * The shell shared by every workspace page: navigation rail, header, and the
 * content column.
 *
 * Each of the five pages previously repeated this structure inline, so a
 * change to the header or the rail meant five edits.
 */
export function AppLayout({
  status,
  children,
  sidebarProps,
  banner = null,
}) {
  return (
    <main className="workspace-page">
      {/* Rendered above the shell so page-level errors are visible without
          scrolling, matching how Tools showed its error banner. */}
      {banner}

      <Sidebar {...sidebarProps} />

      <section className="workspace-main">
        <header className="workspace-header">
          <span className="header-status">
            <span />
            {status}
          </span>

          <div className="header-actions">
            <ProfileMenu />
          </div>
        </header>

        <div className="workspace-content">{children}</div>
      </section>
    </main>
  );
}

export default AppLayout;
