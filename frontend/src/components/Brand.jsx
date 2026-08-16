function Brand({ compact = false }) {
  return (
    <div className={`brand ${compact ? "brand--compact" : ""}`}>
      <div className="brand-mark">✦</div>

      <div className="brand-text">
        <span className="brand-name">WORKMIND</span>

        {!compact && (
          <span className="brand-tagline">
            Your AI productivity workspace
          </span>
        )}
      </div>
    </div>
  );
}

export default Brand;