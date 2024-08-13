// ./frontend/my-app/src/components/AudioManager.js

import React, { useState, useEffect, useCallback } from "react";
import * as api from "../services/api";

const AudioManager = ({ userId, textEntries, voices }) => {
  const [audios, setAudios] = useState([]);
  const [selectedTextEntry, setSelectedTextEntry] = useState("");
  const [selectedVoice, setSelectedVoice] = useState("");

  const fetchUserAudios = useCallback(async () => {
    try {
      const response = await api.getUserAudios(userId);
      setAudios(response.data);
    } catch (error) {
      console.error("Error fetching user audios:", error);
    }
  }, [userId]);

  useEffect(() => {
    fetchUserAudios();
  }, [fetchUserAudios]);

  const handleCreateAudio = async (e) => {
    e.preventDefault();
    if (!selectedTextEntry || !selectedVoice) {
      alert("Please select a text entry and a voice");
      return;
    }
    try {
      const audioData = {
        text_entry_id: parseInt(selectedTextEntry),
        voice_id: parseInt(selectedVoice),
        file_path: "/path/to/audio.mp3",
        duration: 3.5,
        file_size: 1048576,
      };
      console.log("Sending audio data:", audioData);
      const response = await api.createAudio(audioData);
      console.log("Audio created:", response);
      fetchUserAudios();
      setSelectedTextEntry("");
      setSelectedVoice("");
    } catch (error) {
      console.error("Error creating audio:", error);
      alert(`Error creating audio: ${JSON.stringify(error)}`);
    }
  };

  return (
    <div>
      <h2>Audio Management</h2>
      <form onSubmit={handleCreateAudio}>
        <select
          value={selectedTextEntry}
          onChange={(e) => setSelectedTextEntry(e.target.value)}
          required
        >
          <option value="">Select a Text Entry</option>
          {textEntries.map((entry) => (
            <option key={entry.id} value={entry.id}>
              ID: {entry.id} - {entry.content.substring(0, 50)}...
            </option>
          ))}
        </select>
        <select
          value={selectedVoice}
          onChange={(e) => setSelectedVoice(e.target.value)}
          required
        >
          <option value="">Select a Voice</option>
          {voices.map((voice) => (
            <option key={voice.id} value={voice.id}>
              {voice.voice_name}
            </option>
          ))}
        </select>
        <button type="submit">Create Audio</button>
      </form>
      <h3>Your Audios</h3>
      <ul>
        {audios.map((audio) => (
          <li key={audio.id}>
            Text Entry ID: {audio.text_entry_id}, Voice ID: {audio.voice_id},
            Status: {audio.status}, Created At:{" "}
            {new Date(audio.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AudioManager;
