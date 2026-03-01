import axios from "axios";

const api = axios.create({
  baseURL: "https://ai-worker-v4ue.onrender.com", // your Render backend
  headers: {
    "Content-Type": "application/json"
  }
});

export default api;