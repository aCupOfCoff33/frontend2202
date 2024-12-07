Expert Chat Application

Welcome to the Expert Chat Application! This project is a web-based chat interface where two experts engage in a conversation about strategies to eliminate bullying in classrooms. Users can observe the conversation between Expert 1 and Expert 2 or participate by taking on the role of Expert 2. The application leverages FastAPI for the backend and React with Tailwind CSS for the frontend.

Table of Contents

	•	Features
	•	Demo
	•	Technologies Used
	•	Prerequisites
	•	Installation
	•	Backend Setup
	•	Frontend Setup
	•	Running the Application
	•	Starting the Backend Server
	•	Starting the Frontend Application
	•	Usage
	•	Experts Mode
	•	Expert Interaction Mode
	•	Project Structure
	•	Troubleshooting
	•	Contributing
	•	License

Features

	•	Dual Expert Conversation: Watch Expert 1 and Expert 2 discuss effective strategies to eliminate bullying in classrooms.
	•	User Interaction: Switch to Expert Interaction Mode to participate in the conversation as Expert 2.
	•	Real-time Messaging: Messages are dynamically fetched and displayed every 5 seconds in Experts Mode.
	•	Responsive Design: The interface is responsive and user-friendly, ensuring a seamless experience across devices.
	•	Visual Enhancements: Expert 1 messages feature a profile image for better visual distinction.
	•	CORS Configuration: Properly configured to allow smooth communication between frontend and backend.

Demo

Note: Replace the above image with an actual demo GIF showcasing the application.

Technologies Used

	•	Backend:
	•	FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
	•	Transformers: State-of-the-art Natural Language Processing for Pytorch and TensorFlow 2.0.
	•	Sentence Transformers: BERT models for sentence embeddings.
	•	Uvicorn: A lightning-fast ASGI server implementation.
	•	Frontend:
	•	React: A JavaScript library for building user interfaces.
	•	Tailwind CSS: A utility-first CSS framework for rapid UI development.

Prerequisites

Before you begin, ensure you have met the following requirements:
	•	Operating System: Windows, macOS, or Linux.
	•	Python: Version 3.8 or higher.
	•	Node.js & npm: Ensure you have Node.js (v14 or higher) and npm installed.
	•	Git: Installed on your system for cloning the repository.

Installation

Follow these steps to set up the project on your local machine.

Backend Setup

	1.	Clone the Repository

git clone https://github.com/your-username/expert-chat-app.git
cd expert-chat-app/backend


	2.	Create a Virtual Environment
It’s recommended to use a virtual environment to manage dependencies.

python -m venv venv


	3.	Activate the Virtual Environment
	•	Windows

venv\Scripts\activate


	•	macOS/Linux

source venv/bin/activate


	4.	Upgrade pip

pip install --upgrade pip


	5.	Install Backend Dependencies

pip install -r requirements.txt

If a requirements.txt file is not present, install the necessary packages manually:

pip install fastapi uvicorn transformers torch sentence-transformers


	6.	Place the Profile Image
Ensure that the profile image for Expert 1 is placed correctly.
	•	Path: backend/src/assets/prof.JPG
	•	If the assets directory doesn’t exist, create it and place prof.JPG inside.

Frontend Setup

	1.	Navigate to the Frontend Directory

cd ../frontend


	2.	Install Frontend Dependencies

npm install

If you’re using Yarn:

yarn install


	3.	Configure Environment Variables
Create a .env file in the frontend directory to specify the backend API URL.

touch .env

Add the following line to .env:

VITE_API_URL=http://localhost:8000/chat

Note: If you’re not using Vite or have a different setup, adjust accordingly.

	4.	Place the Profile Image
Ensure that the profile image for Expert 1 is correctly referenced in the frontend.
	•	Path: frontend/src/assets/prof.JPG
	•	If the assets directory doesn’t exist, create it and place prof.JPG inside.

Running the Application

Starting the Backend Server

	1.	Navigate to the Backend Directory

cd backend


	2.	Activate the Virtual Environment
	•	Windows

venv\Scripts\activate


	•	macOS/Linux

source venv/bin/activate


	3.	Start the Server

uvicorn backend:app --reload

	•	Parameters:
	•	backend:app: Refers to the app instance in backend.py.
	•	--reload: Enables auto-reloading on code changes. Remove in production.
The server should start at http://localhost:8000.

Starting the Frontend Application

	1.	Navigate to the Frontend Directory

cd ../frontend


	2.	Start the Development Server

npm run dev

If you’re using Yarn:

yarn dev

	•	Default URL: http://localhost:5173
The application should automatically open in your default browser. If not, navigate to the URL manually.

Usage

Experts Mode

	•	Default Mode: Upon launching the application, it starts in Experts Mode.
	•	Functionality:
	•	Expert 1 and Expert 2 engage in a conversation autonomously.
	•	Messages are fetched and displayed every 5 seconds.
	•	Expert 1 messages are left-aligned with a profile image.
	•	Expert 2 messages are right-aligned without an image.
	•	Only the sender labels (Expert 1: or Expert 2:) are bolded; the message text is unbolded.

Expert Interaction Mode

	•	Switching Modes: Click the “Switch to Expert Interaction” button to toggle modes.
	•	Functionality:
	•	You take on the role of Expert 2.
	•	Expert 2 messages appear on the right.
	•	Expert 1 responds on the left with its own messages.
	•	Type your message in the input field and press “Send” or hit Enter to send.
	•	Only the sender labels (Expert 1: or Expert 2:) are bolded; the message text is unbolded.
