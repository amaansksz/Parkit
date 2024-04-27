# Smart Parking System

## Overview

The Smart Parking System automates the process of vehicle parking and gate access control. It uses Python for the backend, React Native for the frontend,
and Firebase for the database. The system enables users to register vehicles and grants access to authorized vehicles through gate control.

## Features

- **User Registration**: Register vehicles with email, password, vehicle type, and license plate number.
- **Gate Access Control**: Utilizes a laptop's camera to scan license plates at the entry gate, granting access if authorized.
- **Exit Validation**: Scans license plates again when exiting, ensuring authorized vehicles exit correctly.

## Prerequisites

Before running the system, ensure the following prerequisites are met:

- Python 3.x installed
- React Native CLI installed
- Firebase account with Firestore database
- NodeMCU configured with a motor for gate control

## Installation

1. Clone this repository.
2. Install Python dependencies in the backend directory:pip install opencv-python pytesseract firebase-admin
3. Install npm packages in the frontend directory:npm install
4. Update Firebase configuration in the frontend code to connect to your Firestore database.

## Usage

### Backend (Python)

1. Run the backend Python script:python license_plate_recognition.py
2. Ensure Firebase Admin SDK is initialized with your service account credentials.

### Frontend (React Native)

1. Run the React Native app:npm start
2. Register vehicles and grant access to authorized vehicles using the app.

## Limitations

- This system simulates parking using a laptop camera and a simulated gate control mechanism, not integrating with actual physical parking infrastructure.

#Note: This is a College Project.








