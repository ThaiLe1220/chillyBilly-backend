// ./frontend/my-app/src/components/AdminVoiceManager.js

import React, { useState, useEffect } from "react";
import * as api from "../services/api";

const AdminVoiceManager = () => {
  const [voices, setVoices] = useState([]);

  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      const response = await api.getAllVoices();
      setVoices(response.data);
    } catch (error) {
      console.error("Error fetching voices:", error);
    }
  };

  const handleCreateDefaults = async () => {
    try {
      await api.createDefaultVoices();
      fetchVoices();
    } catch (error) {
      console.error("Error creating default voices:", error);
    }
  };

  return (
    <div>
      <h2>Voice Management</h2>
      <button onClick={handleCreateDefaults}>Create Default Voices</button>
      <h3>All Voices</h3>
      <ul>
        {voices.map((voice) => (
          <li key={voice.id}>
            {voice.voice_name} - {voice.language} - {voice.status}
            {voice.is_default && " (Default)"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminVoiceManager;
