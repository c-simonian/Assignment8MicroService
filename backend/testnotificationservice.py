import http.client
import json

# Base URL of the microservice
base_url = 'localhost'
port = 5001

# Function to send a notification
def send_notification(message):
    conn = http.client.HTTPConnection(base_url, port)
    headers = {'Content-type': 'application/json'}
    data = json.dumps({'message': message})
    conn.request('POST', '/notify', body=data, headers=headers)
    response = conn.getresponse()
    return response.read().decode()

# Function to get notifications
def get_notifications():
    conn = http.client.HTTPConnection(base_url, port)
    conn.request('GET', '/notifications')
    response = conn.getresponse()
    return response.read().decode()

if __name__ == "__main__":
    # Send a notification
    print("Sending test notification...")
    send_response = send_notification("Test Notification")
    print("Response from send_notification:", send_response)

    # Get notifications
    print("Getting notifications...")
    notifications = get_notifications()
    print("Notifications:", notifications)
