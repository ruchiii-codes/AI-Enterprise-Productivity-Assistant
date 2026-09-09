import { useCallback, useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import "../styles/workspace.css";
import {
  PROVIDERS,
  disconnectIntegration,
  getIntegrationStatus,
  startIntegrationConnect,
} from "../api/integrations";

const LABELS = {
  github: "GitHub",
  gmail: "Gmail",
  calendar: "Calendar",
};

const INITIAL_STATE = {
  github: { connected: false, account: null, loading: true },
  gmail: { connected: false, account: null, loading: true },
  calendar: { connected: false, account: null, loading: true },
};

function Tools() {
  const [error, setError] = useState("");

  // One entry per provider. The three providers previously had three
  // near-identical copies of every piece of state and every handler.
  const [integrations, setIntegrations] = useState(INITIAL_STATE);

  const updateProvider = useCallback((provider, patch) => {
    setIntegrations((current) => ({
      ...current,
      [provider]: { ...current[provider], ...patch },
    }));
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function checkConnections() {
      // Statuses are independent, so fetch them together rather than in
      // sequence as before.
      await Promise.all(
        PROVIDERS.map(async (provider) => {
          try {
            const data = await getIntegrationStatus(provider);

            if (cancelled) return;

            updateProvider(provider, {
              connected: Boolean(data.connected),
              // GitHub returns `username`; Gmail and Calendar return `email`.
              account: data.username ?? data.email ?? null,
              loading: false,
            });
          } catch (requestError) {
            if (cancelled) return;

            updateProvider(provider, {
              connected: false,
              account: null,
              loading: false,
            });

            setError(
              requestError.message ||
                `Unable to check ${LABELS[provider]} connection.`
            );
          }
        })
      );
    }

    checkConnections();

    return () => {
      cancelled = true;
    };
  }, [updateProvider]);

  // -------------------------
  // Connect / disconnect
  // -------------------------
  const connect = async (provider) => {
    setError("");

    try {
      const data = await startIntegrationConnect(provider);

      if (!data?.authorization_url) {
        throw new Error(
          `${LABELS[provider]} did not return an authorization URL.`
        );
      }

      window.location.href = data.authorization_url;
    } catch (requestError) {
      // Previously Gmail and Calendar surfaced this through alert() while
      // GitHub used the inline banner. All three now use the banner.
      setError(
        requestError.message ||
          `Unable to connect ${LABELS[provider]}. Please try again.`
      );
    }
  };

  const disconnect = async (provider) => {
    setError("");

    try {
      await disconnectIntegration(provider);

      updateProvider(provider, { connected: false, account: null });
    } catch (requestError) {
      setError(
        requestError.message ||
          `Unable to disconnect ${LABELS[provider]}. Please try again.`
      );
    }
  };

  const connectGitHub = () => connect("github");
  const disconnectGitHub = () => disconnect("github");
  const connectGmail = () => connect("gmail");
  const disconnectGmail = () => disconnect("gmail");
  const connectCalendar = () => connect("calendar");
  const disconnectCalendar = () => disconnect("calendar");

  // Named bindings kept so the markup below reads unchanged.
  const githubConnected = integrations.github.connected;
  const githubUsername = integrations.github.account;
  const githubLoading = integrations.github.loading;

  const gmailConnected = integrations.gmail.connected;
  const gmailEmail = integrations.gmail.account;
  const gmailLoading = integrations.gmail.loading;

  const calendarConnected = integrations.calendar.connected;
  const calendarEmail = integrations.calendar.account;
  const calendarLoading = integrations.calendar.loading;

  const errorBanner = error ? (
    <div className="tools-error">
      <span>!</span>
      <span>{error}</span>

      <button
        type="button"
        onClick={() => setError("")}
        aria-label="Dismiss error"
      >
        ×
      </button>
    </div>
  ) : null;

  return (
    <AppLayout status="TOOL CONNECTIONS" banner={errorBanner}>
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">CONNECTED TOOLS</span>

              <h1>
                Your tools.
                <br />
                <span>One intelligence layer.</span>
              </h1>

              <p>
                Connect the services you use every day and
                let WorkMind work across them.
              </p>
            </div>
          </section>

          <section className="capability-grid">

            {/* Gmail */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">G</div>
                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">EMAIL</span>

                <h3>Gmail</h3>

                <p>
                  Search and work with your email through
                  WorkMind.
                </p>
              </div>

              <div className="agent-status">
                {gmailLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : gmailConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {gmailEmail && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {gmailEmail}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectGmail}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectGmail}
                    >
                      Connect Gmail
                    </button>
                  </>
                )}
              </div>
            </div>

            {/* Calendar */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">C</div>
                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">SCHEDULE</span>

                <h3>Calendar</h3>

                <p>
                  Access and manage your schedule through
                  WorkMind.
                </p>
              </div>

              <div className="agent-status">
                {calendarLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : calendarConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {calendarEmail && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {calendarEmail}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectCalendar}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectCalendar}
                    >
                      Connect Calendar
                    </button>
                  </>
                )}
              </div>
            </div>

            {/* GitHub */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">GH</div>

                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">DEVELOPMENT</span>

                <h3>GitHub</h3>

                <p>
                  Search repositories, issues, and development
                  activity.
                </p>
              </div>

              <div className="agent-status">
                {githubLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : githubConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {githubUsername && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {githubUsername}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectGitHub}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectGitHub}
                    >
                      Connect GitHub
                    </button>
                  </>
                )}
              </div>
            </div>

          </section>
    </AppLayout>
  );
}

export default Tools;