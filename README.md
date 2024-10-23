# AR Sales Assistant

The AR Sales Assistant is an augmented reality project that interacts with users via voice commands, offering sales assistance in a dynamic and engaging way. This project leverages voice input, AR animations, and backend processing to create an interactive sales experience.

## Project Overview

The AR Sales Assistant allows users to:
- Use voice commands to interact with the AR assistant.
- Receive real-time responses and animations based on user input.
- Seamlessly integrate voice recognition and AR technologies.

This project is built using multiple technologies, including Unity for the AR interface, Azure Kubernetes Service (AKS) for cloud infrastructure, and Docker for containerization.

## Key Features

- **Voice Command Interaction**: Users can give voice commands, which are processed by the backend, triggering appropriate responses and AR animations.
- **Real-Time Response**: The backend returns a text response along with an animation name, which is then displayed in the AR environment.
- **Containerized Backend**: Docker containers manage the backend services, ensuring scalability and easy deployment.
- **Cloud Infrastructure**: The application runs on Azure Kubernetes Service (AKS), providing high availability and scalability.

## Technology Stack

- **Frontend**: Unity (for AR and voice interaction)
- **Backend**: Flask-based API for processing requests
- **Containerization**: Docker
- **Cloud Platform**: Azure Kubernetes Service (AKS)
- **API**: Custom APIs for handling voice input, generating responses, and managing AR animations
- **Azure Blob Storage**: For storing assets and files related to the project

## Project Structure
├── AR-Sale-Assistant/ │ ├── UnityProject/ # AR and voice interaction code │ ├── Backend/ # Flask backend for processing requests │ ├── Docker/ # Docker configuration and setup │ ├── AKS/ # Scripts and configuration for AKS deployment │ ├── README.md # Project documentation


## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/SAIMA-Team/AR-Sale-Assistant.git
    cd AR-Sale-Assistant
    ```

2. **Backend Setup**:
    - Navigate to the `Backend/` directory.
    - Install the required Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Start the Flask backend:
        ```bash
        python app.py
        ```

3. **Docker Setup**:
    - Build the Docker image for the backend:
        ```bash
        docker build -t ar-sale-assistant-backend .
        ```
    - Run the Docker container:
        ```bash
        docker run -p 5000:5000 ar-sale-assistant-backend
        ```

4. **Azure Kubernetes Service (AKS) Setup**:
    - Deploy the Docker containers to AKS using the provided deployment scripts in the `AKS/` directory.

## Usage

- Launch the Unity AR application.
- Use the "ASK" button to record your voice commands.
- The voice input will be sent to the backend, processed, and the AR assistant will respond with text and an animation.
  
## API Endpoints

- **POST /process**: Process the user's voice input and return a response.
- **GET /audio**: Retrieve the generated audio response for playback in the AR app.

## Future Enhancements

- Improved NLP for better voice command recognition.
- More AR animations to enhance user engagement.
- Integration with external sales databases for real-time product information.


## Contributors

- **Sachindu D Weerakkodi** (Backend and Infrastructure)
- **SAIMA Team** (Core Development and AR Integration)

---

Feel free to explore and contribute to this project by submitting issues or pull requests!


