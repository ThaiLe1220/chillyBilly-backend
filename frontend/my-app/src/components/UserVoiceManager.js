// ./frontend/my-app/src/components/UserVoiceManager.js
import React, { useState, useEffect, useCallback } from "react";
import * as api from "../services/api";

const UserVoiceManager = ({ userId }) => {
  const [voices, setVoices] = useState([]);
  const [newVoice, setNewVoice] = useState({
    voice_name: "",
    language: "en",
    description: "",
    original_file_path: "",
  });

  const fetchUserVoices = useCallback(async () => {
    try {
      const response = await api.getUserVoices(userId);
      setVoices(response.data);
    } catch (error) {
      console.error("Error fetching user voices:", error);
    }
  }, [userId]);

  useEffect(() => {
    fetchUserVoices();
  }, [fetchUserVoices]);
  const handleInputChange = (e) => {
    setNewVoice({ ...newVoice, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createUserVoice(userId, newVoice);
      setNewVoice({
        voice_name: "",
        language: "en",
        description: "",
        original_file_path: "",
      });
      fetchUserVoices();
    } catch (error) {
      console.error("Error creating user voice:", error);
    }
  };

  return (
    <div>
      <h2>Your Voices</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="voice_name"
          value={newVoice.voice_name}
          onChange={handleInputChange}
          placeholder="Voice Name"
          required
        />
        <select
          name="language"
          value={newVoice.language}
          onChange={handleInputChange}
        >
          <option value="en">English</option>
          <option value="vi">Vietnamese</option>
        </select>
        <input
          name="description"
          value={newVoice.description}
          onChange={handleInputChange}
          placeholder="Description"
        />
        <input
          name="original_file_path"
          value={newVoice.original_file_path}
          onChange={handleInputChange}
          placeholder="Path to voice file"
          required
        />
        <button type="submit">Create Voice</button>
      </form>
      <h3>Your Custom Voices</h3>
      <ul>
        {voices.map((voice) => (
          <li key={voice.id}>
            {voice.voice_name} - {voice.language} - {voice.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserVoiceManager;
