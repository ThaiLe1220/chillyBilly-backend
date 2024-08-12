// ./frontend/my-app/src/components/UserList.js

import React from 'react';

function UserList({ users, onDeleteUser }) {
  return (
    <div>
      <h2>User List</h2>
      <table>
        <thead>
          <tr>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>ID</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Username</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Email</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Two Factor Enabled</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Is Active</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Role</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Created At</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Updated At</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Last Login</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Last Active Date</th>
            <th style={{ border: '1px solid black', fontSize: '16px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.id}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.username}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.email}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.two_factor_enabled ? 'Yes' : 'No'}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.is_active ? 'Yes' : 'No'}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.role}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{new Date(user.created_at).toLocaleString()}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{new Date(user.updated_at).toLocaleString()}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.last_login ? new Date(user.last_login).toLocaleString() : 'N/A'}</td>
              <td style={{ border: '1px solid black', fontSize: '12px' }}>{user.last_active_date ? new Date(user.last_active_date).toLocaleString() : 'N/A'}</td>
              <td>
                <button onClick={() => onDeleteUser(user.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserList;