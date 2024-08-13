// ./frontend/my-app/src/components/ProfileManager.js

import React, { useState, useEffect, useCallback } from "react";
import * as api from "../services/api";

const ProfileManager = ({ userId, isAdminView }) => {
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    date_of_birth: "",
    preferred_language: "vi",
  });

  const fetchProfile = useCallback(async () => {
    try {
      const response = await api.getProfile(userId);
      setProfile(response.data);
      setFormData(response.data);
    } catch (error) {
      console.error("Error fetching profile:", error);
    }
  }, [userId]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form data
    if (formData.first_name.trim() === "") {
      alert("Please enter your first name.");
      return;
    }

    if (formData.last_name.trim() === "") {
      alert("Please enter your last name.");
      return;
    }

    if (formData.date_of_birth.trim() === "") {
      alert("Please enter your date of birth.");
      return;
    }

    if (formData.preferred_language.trim() === "") {
      alert("Please select your preferred language.");
      return;
    }

    try {
      if (profile) {
        await api.updateProfile(userId, formData);
      } else {
        await api.createProfile(userId, formData);
      }
      fetchProfile();
      setIsEditing(false);
    } catch (error) {
      console.error("Error saving profile:", error);
    }
  };

  if (!profile && !isEditing) {
    return (
      <div>
        <h2>No Profile Found</h2>
        <button onClick={() => setIsEditing(true)}>Create Profile</button>
      </div>
    );
  }

  if (isEditing) {
    return (
      <form onSubmit={handleSubmit}>
        <h2>{profile ? "Edit Profile" : "Create Profile"}</h2>
        <input
          name="first_name"
          value={formData.first_name}
          onChange={handleInputChange}
          placeholder="First Name"
        />
        <input
          name="last_name"
          value={formData.last_name}
          onChange={handleInputChange}
          placeholder="Last Name"
        />
        <input
          type="date"
          name="date_of_birth"
          value={formData.date_of_birth.split("T")[0]}
          onChange={handleInputChange}
        />
        <select
          name="preferred_language"
          value={formData.preferred_language}
          onChange={handleInputChange}
        >
          <option value="en">English</option>
          <option value="vi">Vietnamese</option>
        </select>
        <button type="submit">Save</button>
        <button type="button" onClick={() => setIsEditing(false)}>
          Cancel
        </button>
      </form>
    );
  }

  return (
    <div>
      <h2>User Profile</h2>
      <p>First Name: {profile.first_name}</p>
      <p>Last Name: {profile.last_name}</p>
      <p>
        Date of Birth: {new Date(profile.date_of_birth).toLocaleDateString()}
      </p>
      <p>Preferred Language: {profile.preferred_language}</p>
      <button onClick={() => setIsEditing(true)}>Edit Profile</button>

      {!isAdminView && (
        <button onClick={() => setIsEditing(true)}>Edit Profile</button>
      )}
    </div>
  );
};

export default ProfileManager;
