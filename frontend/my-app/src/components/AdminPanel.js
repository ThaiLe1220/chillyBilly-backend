// ./frontend/my-app/src/components/AdminPanel.js

import React, { useState, useEffect } from "react";
import * as api from "../services/api";
import UserList from "./UserList";
import UpdateUserForm from "./UpdateUserForm";
import GuestManagement from "./GuestManagement";
import ProfileManager from "./ProfileManager";
import TextEntryManager from "./TextEntryManager";
import AdminVoiceManager from "./AdminVoiceManager";

const AdminPanel = ({ currentUser, onLogout }) => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const handleDeleteUser = async (id) => {
    try {
      await api.deleteUser(id);
      fetchUsers();
      if (selectedUser && selectedUser.id === id) {
        setSelectedUser(null);
      }
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  const handleUpdateUser = async (updatedUser) => {
    try {
      await api.updateUser(updatedUser.id, updatedUser);
      fetchUsers();
      if (selectedUser && selectedUser.id === updatedUser.id) {
        setSelectedUser(updatedUser);
      }
    } catch (error) {
      console.error("Error updating user:", error);
    }
  };

  const handleSelectUser = (user) => {
    setSelectedUser(user);
  };

  return (
    <div>
      <h1>Admin Panel</h1>
      <p>Welcome, Admin {currentUser.username}!</p>
      <button onClick={onLogout}>Logout</button>

      <div style={{ display: "flex" }}>
        <div style={{ flex: 1 }}>
          <UpdateUserForm onUpdateUser={handleUpdateUser} />
          <UserList
            users={users}
            onDeleteUser={handleDeleteUser}
            onSelectUser={handleSelectUser}
          />
          <GuestManagement />
          <AdminVoiceManager />
        </div>

        {selectedUser && (
          <div style={{ flex: 1 }}>
            <h2>Selected User: {selectedUser.username}</h2>
            <ProfileManager userId={selectedUser.id} isAdminView={true} />
            <TextEntryManager userId={selectedUser.id} isAdminView={true} />
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;
