import axios from "axios";

const api = axios.create({
  baseURL: "https://ai-worker-v4ue.onrender.com"
});

export default api;