import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  CONVERSATION_STORAGE_KEY,
  THEME_STORAGE_KEY,
} from "../../config/env";
import { useAuth } from "../../hooks/useAuth";

function ProfileMenu() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [isOpen, setIsOpen] = useState(false);
  const [theme, setTheme] = useState(
    () => localStorage.getItem(THEME_STORAGE_KEY) || "dark"
  );

  const menuRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);
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
    logout();
    localStorage.removeItem(CONVERSATION_STORAGE_KEY);

    // Client-side navigation rather than a full page reload.
    navigate("/login", { replace: true });
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