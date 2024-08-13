// ./frontend/my-app/src/App.js
import React, { useState, useEffect } from "react";
import AuthForm from "./components/AuthForm";
import RegularUserView from "./components/RegularUserView";
import AdminPanel from "./components/AdminPanel";

function App() {
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const user = JSON.parse(localStorage.getItem("user"));
      setCurrentUser(user);
    }
  }, []);

  const handleLogin = (user) => {
    setCurrentUser(user);
    localStorage.setItem("user", JSON.stringify(user));
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  if (!currentUser) {
    return <AuthForm onLogin={handleLogin} />;
  }

  if (currentUser.role === "REGULAR") {
    return (
      <div className="App">
        <RegularUserView user={currentUser} />
        <button onClick={handleLogout}>Logout</button>
      </div>
    );
  }

  return (
    <div className="App">
      <AdminPanel currentUser={currentUser} onLogout={handleLogout} />
    </div>
  );
}

export default App;
