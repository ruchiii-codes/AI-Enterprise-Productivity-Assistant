import Field from "./Field";

/**
 * A Field with a show/hide toggle.
 *
 * Visibility is controlled by the caller rather than held here, because
 * ResetPassword deliberately drives its password and confirm inputs from a
 * single toggle.
 *
 * The toggle always carries an aria-label. When this markup was copied into
 * each page, Login's copy had one and Register's two did not -- the sort of
 * drift that duplicated markup produces and a shared component prevents.
 */
function PasswordField({ visible, onToggleVisibility, ...props }) {
  return (
    <Field
      {...props}
      type={visible ? "text" : "password"}
      trailing={
        <button
          type="button"
          className="password-toggle"
          onClick={onToggleVisibility}
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? "Hide" : "Show"}
        </button>
      }
    />
  );
}

export default PasswordField;
