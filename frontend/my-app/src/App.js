// ./frontend/my-app/src/App.js

import React, { useState, useEffect } from 'react';
import * as api from './services/api';
import UserList from './components/UserList';
import UpdateUserForm from './components/UpdateUserForm';
import GuestManagement from './components/GuestManagement';
import AuthForm from './components/AuthForm';
import RegularUserView from './components/RegularUserView';

function App() {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const user = JSON.parse(localStorage.getItem('user'));
      setCurrentUser(user);
      if (user.role === 'ADMIN') {
        fetchUsers();
      }
    }
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleDeleteUser = async (id) => {
    try {
      await api.deleteUser(id);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleUpdateUser = async (updateUser) => {
    try {
      await api.updateUser(updateUser.id, updateUser);
      fetchUsers();
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  const handleLogin = (user) => {
    setCurrentUser(user);
    localStorage.setItem('user', JSON.stringify(user));
    if (user.role === 'ADMIN') {
      fetchUsers();
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUsers([]);
  };

  if (!currentUser) {
    return <AuthForm onLogin={handleLogin} />;
  }

  if (currentUser.role === 'REGULAR') {
    return (
      <div className="App">
        <RegularUserView user={currentUser} />
        <button onClick={handleLogout}>Logout</button>
      </div>
    );
  }

  return (
    <div className="App">
      <h1>Face Swap User Management</h1>
      <p>Welcome, Admin {currentUser.username}!</p>
      <button onClick={handleLogout}>Logout</button>
      <UpdateUserForm onUpdateUser={handleUpdateUser} />
      <UserList users={users} onDeleteUser={handleDeleteUser} />
      <GuestManagement />
    </div>
  );
}

export default App;