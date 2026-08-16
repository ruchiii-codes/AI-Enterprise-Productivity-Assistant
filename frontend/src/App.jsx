import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Workspace from "./pages/Workspace";
import Knowledge from "./pages/Knowledge";
import Agents from "./pages/Agents";
import Tools from "./pages/Tools";
import Settings from "./pages/Settings";
import Chat from "./pages/Chat";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/workspace" element={<Workspace />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/knowledge" element={<Knowledge />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/tools" element={<Tools />} />
        <Route path="/settings" element={<Settings />} />

        <Route
          path="*"
          element={<Navigate to="/login" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;