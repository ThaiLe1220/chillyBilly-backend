import React, { useState, useEffect, useCallback } from "react";
import ProfileManager from "./ProfileManager";
import TextEntryManager from "./TextEntryManager";
import UserVoiceManager from "./UserVoiceManager";
import AudioManager from "./AudioManager";
import * as api from "../services/api";

const RegularUserView = ({ user }) => {
  const [textEntries, setTextEntries] = useState([]);
  const [voices, setVoices] = useState([]);

  const fetchTextEntries = useCallback(async () => {
    try {
      const response = await api.getUserTextEntries(user.id);
      setTextEntries(response.data);
    } catch (error) {
      console.error("Error fetching text entries:", error);
    }
  }, [user.id]);

  const fetchVoices = useCallback(async () => {
    try {
      const response = await api.getAllVoices();
      setVoices(response.data);
    } catch (error) {
      console.error("Error fetching voices:", error);
    }
  }, []);

  useEffect(() => {
    fetchTextEntries();
    fetchVoices();
  }, [fetchTextEntries, fetchVoices]); // Include the functions in the dependency array

  return (
    <div>
      <h1>Welcome, {user.username}!</h1>
      <ProfileManager userId={user.id} />
      <TextEntryManager userId={user.id} />
      <UserVoiceManager userId={user.id} />
      <AudioManager
        userId={user.id}
        textEntries={textEntries}
        voices={voices}
      />
    </div>
  );
};

export default RegularUserView;
