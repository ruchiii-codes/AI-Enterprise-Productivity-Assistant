import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setMessage(response.data.message);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail);
      } else {
        setMessage("Upload failed.");
      }
    }
  };

  return (
    <div className="container">
      <h1>AI Enterprise Productivity Assistant 🚀</h1>

      <div className="upload-card">
        <h2>Upload PDF</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        />

        <button onClick={handleUpload}>
          Upload
        </button>

        {message && (
          <p>{message}</p>
        )}
      </div>
    </div>
  );
}

export default App;