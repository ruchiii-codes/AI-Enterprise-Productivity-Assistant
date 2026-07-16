import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/health")
      .then((response) => {
        setStatus(response.data.status);
      })
      .catch(() => {
        setStatus("Backend not running");
      });
  }, []);

  return (
    <div className="container">
      <h1>AI Enterprise Productivity Assistant 🚀</h1>

      <h2>Backend Status</h2>

      <p>{status}</p>
    </div>
  );
}

export default App;