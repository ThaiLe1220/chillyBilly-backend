// ./frontend/my-app/src/components/UpdateUserForm.js

import React, { useState } from 'react';

function UpdateUserForm({ onUpdateUser }) {
  const [updateUser, setUpdateUser] = useState({
    id: '',
    username: '',
    email: '',
    password: '',
    two_factor_enabled: false,
    is_active: true,
    role: 'REGULAR'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdateUser(updateUser);
    setUpdateUser({
      id: '',
      username: '',
      email: '',
      password: '',
      two_factor_enabled: false,
      is_active: true,
      role: 'REGULAR'
    });
  };

  return (
    <div>
      <h2>Update User</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="User ID"
          value={updateUser.id}
          onChange={(e) => setUpdateUser({ ...updateUser, id: e.target.value })}
        />
        <input
          type="text"
          placeholder="Username"
          value={updateUser.username}
          onChange={(e) => setUpdateUser({ ...updateUser, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          value={updateUser.email}
          onChange={(e) => setUpdateUser({ ...updateUser, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          value={updateUser.password}
          onChange={(e) => setUpdateUser({ ...updateUser, password: e.target.value })}
        />
        <label>
          Two Factor Enabled:
          <input
            type="checkbox"
            checked={updateUser.two_factor_enabled}
            onChange={(e) => setUpdateUser({ ...updateUser, two_factor_enabled: e.target.checked })}
          />
        </label>
        <label>
          Is Active:
          <input
            type="checkbox"
            checked={updateUser.is_active}
            onChange={(e) => setUpdateUser({ ...updateUser, is_active: e.target.checked })}
          />
        </label>
        <select
          value={updateUser.role}
          onChange={(e) => setUpdateUser({ ...updateUser, role: e.target.value })}
        >
          <option value="REGULAR">Regular</option>
          <option value="ADMIN">Admin</option>
        </select>
        <button type="submit">Update User</button>
      </form>
    </div>
  );
}

export default UpdateUserForm;