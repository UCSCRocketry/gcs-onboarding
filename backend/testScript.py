#!/usr/bin/env python3
"""
Test script to trigger update_data() function and see print output
"""
import socketio
import time

# socketIO client
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def send_data_HIGH_G_ACCEL(data):
    print(f"Received data: {data}")

if __name__ == "__main__":
    try:
        print("Starting test...")
        print("Connecting to http://127.0.0.1:9999...")
        
        # connect to the server
        sio.connect('http://127.0.0.1:9999')
        
        time.sleep(5)  # wait 5 seconds to see multiple updates
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sio.disconnect()
