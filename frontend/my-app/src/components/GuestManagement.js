// ./frontend/my-app/src/components/GuestManagement.js

import React, { useState, useEffect } from "react";
import * as api from "../services/api";

function GuestManagement() {
  const [guests, setGuests] = useState([]);
  const [selectedGuest, setSelectedGuest] = useState(null);

  useEffect(() => {
    fetchGuests();
  }, []);

  const fetchGuests = async () => {
    try {
      const response = await api.getGuests();
      setGuests(response.data);
    } catch (error) {
      console.error("Error fetching guests:", error);
    }
  };

  const handleCreateGuest = async () => {
    try {
      const response = await api.createGuest();
      setGuests([...guests, response.data]);
    } catch (error) {
      console.error("Error creating guest:", error);
    }
  };

  const handleGetGuest = async (id) => {
    try {
      const response = await api.getGuest(id);
      setSelectedGuest(response.data);
    } catch (error) {
      console.error("Error fetching guest:", error);
    }
  };

  const handleUpdateGuest = async (id) => {
    try {
      const response = await api.updateGuest(id);
      setGuests(
        guests.map((guest) => (guest.id === id ? response.data : guest))
      );
    } catch (error) {
      console.error("Error updating guest:", error);
    }
  };

  const handleDeleteGuest = async (id) => {
    try {
      await api.deleteGuest(id);
      setGuests(guests.filter((guest) => guest.id !== id));
    } catch (error) {
      console.error("Error deleting guest:", error);
    }
  };

  const handleCleanupGuests = async () => {
    try {
      const response = await api.cleanupGuests();
      console.log(response.data.message);
      fetchGuests();
    } catch (error) {
      console.error("Error cleaning up guests:", error);
    }
  };

  return (
    <div>
      <h2>Guest Management</h2>
      <button onClick={handleCreateGuest}>Create Guest</button>
      <button onClick={handleCleanupGuests}>Cleanup Inactive Guests</button>

      <h3>Guest List</h3>
      {guests.length === 0 ? (
        <p>No guests.</p>
      ) : (
        <ul>
          {guests.map((guest) => (
            <li key={guest.id}>
              ID: {guest.id} - Created:{" "}
              {new Date(guest.created_at).toLocaleString()}
              <button onClick={() => handleGetGuest(guest.id)}>View</button>
              <button onClick={() => handleUpdateGuest(guest.id)}>
                Update Activity
              </button>
              <button onClick={() => handleDeleteGuest(guest.id)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}

      {selectedGuest && (
        <div>
          <h3>Selected Guest Details</h3>
          <p>ID: {selectedGuest.id}</p>
          <p>
            Created At: {new Date(selectedGuest.created_at).toLocaleString()}
          </p>
          <p>
            Last Active:{" "}
            {new Date(selectedGuest.last_active_date).toLocaleString()}
          </p>
          <p>
            Expires: {new Date(selectedGuest.expiration_date).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}

export default GuestManagement;
