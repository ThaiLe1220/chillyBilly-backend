// ./frontend/my-app/src/components/RegularUserView.js

import React from 'react';

function RegularUserView({ user }) {
  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <p>User Information:</p>
      <ul>
        <li>ID: {user.id}</li>
        <li>Email: {user.email}</li>
        <li>Role: {user.role}</li>
        <li>Active: {user.is_active ? 'Yes' : 'No'}</li>
        <li>Created At: {new Date(user.created_at).toLocaleString()}</li>
        <li>Last Login: {user.last_login ? new Date(user.last_login).toLocaleString() : 'N/A'}</li>
      </ul>
    </div>
  );
}

export default RegularUserView;