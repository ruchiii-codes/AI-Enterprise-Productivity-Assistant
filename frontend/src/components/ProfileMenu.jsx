import { useEffect, useRef, useState } from "react";
import { getCurrentUser } from "../services/authService";

function ProfileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState(
    localStorage.getItem("workmind_theme") || "dark"
  );

  const menuRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    getCurrentUser(token)
      .then(setUser)
      .catch(() => {
        setUser(null);
      });
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("workmind_theme", theme);
  }, [theme]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("workmind_conversation_id");
    window.location.href = "/login";
  };

  const displayName = user?.username || "User";
  const email = user?.email || "";
  const initials = displayName
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="profile-menu-wrapper" ref={menuRef}>
      <button
        className="user-avatar profile-avatar-button"
        onClick={() => setIsOpen((prev) => !prev)}
        title="Account"
      >
        {initials || "U"}
      </button>

      {isOpen && (
        <div className="profile-menu">
          <div className="profile-menu-user">
            <div className="profile-menu-avatar">
              {initials || "U"}
            </div>

            <div className="profile-menu-user-info">
              <strong>{displayName}</strong>
              <span>{email}</span>
            </div>
          </div>

          <div className="profile-menu-divider" />

          <div className="profile-menu-theme">
            <button
              className={theme === "light" ? "active" : ""}
              onClick={() => setTheme("light")}
            >
              <span>☀</span>
              Light mode
            </button>

            <button
              className={theme === "dark" ? "active" : ""}
              onClick={() => setTheme("dark")}
            >
              <span>◐</span>
              Dark mode
            </button>
          </div>

          <div className="profile-menu-divider" />

          <button
            className="profile-menu-logout"
            onClick={handleLogout}
          >
            <span>↪</span>
            Log out
          </button>
        </div>
      )}
    </div>
  );
}

export default ProfileMenu;