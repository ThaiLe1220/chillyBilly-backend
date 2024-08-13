// ./frontend/my-app/src/components/TextEntryManager.js

import React, { useState, useEffect, useCallback } from "react";
import * as api from "../services/api";

const TextEntryManager = ({ userId, isAdminView }) => {
  const [textEntries, setTextEntries] = useState([]);
  const [newEntry, setNewEntry] = useState({ content: "", language: "en" });

  const fetchTextEntries = useCallback(async () => {
    try {
      const response = await api.getUserTextEntries(userId);
      setTextEntries(response.data);
    } catch (error) {
      console.error("Error fetching text entries:", error);
    }
  }, [userId]);

  useEffect(() => {
    fetchTextEntries();
  }, [fetchTextEntries]);

  const handleInputChange = (e) => {
    setNewEntry({ ...newEntry, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createTextEntry({ ...newEntry, user_id: userId });
      setNewEntry({ content: "", language: "en" });
      fetchTextEntries();
    } catch (error) {
      console.error("Error creating text entry:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteTextEntry(id);
      fetchTextEntries();
    } catch (error) {
      console.error("Error deleting text entry:", error);
    }
  };

  return (
    <div>
      <h2>Text Entries</h2>
      {!isAdminView && (
        <form onSubmit={handleSubmit}>
          <textarea
            name="content"
            value={newEntry.content}
            onChange={handleInputChange}
            placeholder="Enter your text here"
            required
          />
          <select
            name="language"
            value={newEntry.language}
            onChange={handleInputChange}
          >
            <option value="en">English</option>
            <option value="vi">Vietnamese</option>
            {/* Add more language options as needed */}
          </select>
          <button type="submit">Add Entry</button>
        </form>
      )}

      <ul>
        {textEntries.map((entry) => (
          <li key={entry.id}>
            <p>
              <strong>ID: {entry.id}</strong>
            </p>
            <p>{entry.content}</p>
            <p>Language: {entry.language}</p>
            <p>Created at: {new Date(entry.created_at).toLocaleString()}</p>
            {!isAdminView && (
              <button onClick={() => handleDelete(entry.id)}>Delete</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TextEntryManager;
