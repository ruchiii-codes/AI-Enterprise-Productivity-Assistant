/**
 * One labelled input in the auth forms.
 *
 * This markup -- label, icon, input, optional hint -- was repeated nine times
 * across Login, Register, ForgotPassword and ResetPassword.
 *
 * Any prop not named here is forwarded to the <input>, so callers pass type,
 * name, value, onChange, placeholder, required and minLength exactly as they
 * did when the markup was inline.
 *
 * `labelAction` renders beside the label (Login's "Forgot password?" link).
 * `trailing` renders inside the input wrapper, after the input, and is how
 * PasswordField attaches its show/hide toggle.
 */
function Field({
  id,
  label,
  icon,
  hint,
  labelAction,
  trailing,
  ...inputProps
}) {
  return (
    <div className="field">
      {labelAction ? (
        <div className="field-label-row">
          <label htmlFor={id}>{label}</label>
          {labelAction}
        </div>
      ) : (
        <label htmlFor={id}>{label}</label>
      )}

      <div className="input-wrap">
        <span className="input-icon">{icon}</span>

        <input id={id} {...inputProps} />

        {trailing}
      </div>

      {hint && <small className="field-hint">{hint}</small>}
    </div>
  );
}

export default Field;
