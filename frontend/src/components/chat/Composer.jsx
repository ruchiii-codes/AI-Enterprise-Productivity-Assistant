/**
 * The message composer: upload control, textarea and send button, plus the
 * upload progress indicator.
 *
 * Presentational.
 */
export function Composer({
  message,
  sending,
  uploading,
  onMessageChange,
  onSubmit,
  onFileUpload,
}) {
  const setMessage = onMessageChange;
  const handleSubmit = onSubmit;
  const handleFileUpload = onFileUpload;

  return (
    <div className="chat-composer-area">

          {uploading && (
            <div className="upload-status">
              <span className="upload-status-icon">↑</span>
              <span>Uploading document...</span>
              <span className="upload-status-dots">
                <i />
                <i />
                <i />
              </span>
            </div>
          )}

          <form
            className="chat-composer"
            onSubmit={handleSubmit}
          >

            <label
              className={`composer-action ${uploading ? "uploading" : ""}`}
              title="Upload document"
            >
              {uploading ? "↑" : "+"}
            
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileUpload}
                disabled={uploading || sending}
                hidden
              />
            </label>

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {
                  event.preventDefault();
                  handleSubmit(event);
                }
              }}
              placeholder="Ask WorkMind anything..."
              rows={1}
            />

            <button
              type="submit"
              className="composer-send"
              disabled={
                !message.trim() ||
                sending
              }
            >

              {sending ? "..." : "↑"}
            </button>

          </form>

          <div className="composer-hint">
            <span>WorkMind can make mistakes.</span>
            <span>Check important information.</span>
          </div>

    </div>
  );
}

export default Composer;
