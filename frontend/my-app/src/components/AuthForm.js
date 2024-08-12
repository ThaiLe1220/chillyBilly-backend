// ./frontend/my-app/src/components/AuthForm.js

import React, { useState } from 'react';
import * as api from '../services/api';

function AuthForm({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ username: '', email: '', password: '', role: 'REGULAR' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear any previous errors
    try {
      if (isLogin) {
        const response = await api.login(credentials);
        localStorage.setItem('token', response.data.access_token);
        onLogin(response.data.user);
      } else {
        await api.createUser(credentials);
        // After successful registration, log the user in
        const loginResponse = await api.login({ username: credentials.username, password: credentials.password });
        localStorage.setItem('token', loginResponse.data.access_token);
        onLogin(loginResponse.data.user);
      }
    } catch (error) {
      console.error(isLogin ? 'Login failed:' : 'Registration failed:', error);
      if (error.response && error.response.data && error.response.data.detail) {
        setError(error.response.data.detail);
      } else if (error.response && error.response.status === 400) {
        setError('Username already exists. Please choose a different username.');
      } else {
        setError(isLogin ? 'Login failed. Please check your credentials.' : 'Registration failed. Please try again.');
      }
    }
  };

  return (
    <div>
      <h2>{isLogin ? 'Login' : 'Register'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          required
        />
        {!isLogin && (
          <>
            <input
              type="email"
              placeholder="Email"
              value={credentials.email}
              onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
              required
            />
            <select
              value={credentials.role}
              onChange={(e) => setCredentials({ ...credentials, role: e.target.value })}
            >
              <option value="REGULAR">Regular</option>
              <option value="ADMIN">Admin</option>
            </select>
          </>
        )}
        <input
          type="password"
          placeholder="Password"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          required
        />
        <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
      </form>
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Need to register?' : 'Already have an account?'}
      </button>
    </div>
  );
}

export default AuthForm;