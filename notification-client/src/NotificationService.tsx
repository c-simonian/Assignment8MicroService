import React, { useState, useEffect } from 'react';
import './NotificationService.css';

const NotificationService: React.FC = () => {
  const [notifications, setNotifications] = useState<string[]>([]);
  const [showPopup, setShowPopup] = useState<boolean>(false);
  const [popupMessage, setPopupMessage] = useState<string>('');

  const fetchNotifications = async () => {
    try {
      const response = await fetch('http://localhost:5001/notifications');
      const data = await response.json();
      setNotifications(data.map((notification: { message: string }) => notification.message));
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    }
  };

  const sendNotification = async () => {
    try {
      const response = await fetch('http://localhost:5001/notify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'Conversion has been completed' }),
      });
      if (response.ok) {
        setPopupMessage('Conversion has been completed');
        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 3000); // Hide after 3 seconds
        fetchNotifications();
      }
    } catch (error) {
      console.error('Failed to send notification:', error);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <div>
      <h1>Notification Service</h1>
      <button onClick={sendNotification}>Notify Conversion Completion</button>
      {showPopup && (
        <div className="notification-popup">
          {popupMessage}
        </div>
      )}
      <div>
        <h2>Notifications</h2>
        <ul>
          {notifications.map((notification, index) => (
            <li key={index}>{notification}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default NotificationService;
