import { Component } from "react";

/**
 * Catches render errors anywhere below it.
 *
 * Without a boundary, a single thrown error unmounts the whole tree and the
 * user is left staring at a blank white page with no way forward.
 *
 * Must be a class: there is no hook equivalent of componentDidCatch.
 */
export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    // Kept as console.error rather than swallowed: this is the only record of
    // the failure until real error reporting is wired up.
    console.error("Unhandled render error:", error, info?.componentStack);
  }

  handleReload = () => {
    window.location.assign("/");
  };

  render() {
    const { error } = this.state;

    if (!error) {
      return this.props.children;
    }

    return (
      <main className="auth-page">
        <section className="auth-shell">
          <div className="auth-form-panel">
            <div className="auth-form-container">
              <div className="form-heading">
                <span className="form-kicker">SOMETHING WENT WRONG</span>

                <h2>This page hit an error</h2>

                <p>
                  The rest of WorkMind is unaffected. Reloading usually
                  clears it.
                </p>
              </div>

              {import.meta.env.DEV && (
                <div className="auth-error">{String(error)}</div>
              )}

              <button
                type="button"
                className="auth-submit"
                onClick={this.handleReload}
              >
                <span>Reload WorkMind</span>
                <span className="submit-arrow">→</span>
              </button>
            </div>
          </div>
        </section>
      </main>
    );
  }
}

export default ErrorBoundary;
