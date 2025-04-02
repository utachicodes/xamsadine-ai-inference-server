# Xamsadine AI - Inference Server

## Overview
The Xamsadine AI Inference Server is a core component of the **Xamsadine AI** system, responsible for processing voice-based queries. It receives WAV audio files, performs inference, and returns the processed text output. This server plays a crucial role in enabling the chatbot to understand and respond to spoken queries.

As part of the setup, 5 test audio files in WAV format have been provided to ensure proper functionality and testing.

## Features
- **Processes voice-based queries** using WAV format.
- **REST API** for seamless integration.
- **Dockerized** for easy deployment.

## Setup & Usage

### Prerequisites
- Docker installed on your system.
- Test audios in WAV format (5 provided).

### Running the Server
1. **Locate the server folder:**
   ```sh
   cd xamsadine-inference-server
   ```
2. **Build the Docker image:**
   ```sh
   docker build -t image-name .
   ```
3. **Run the server:**
   ```sh
   docker run -p 8080:8080 -e HF_TOKEN=your_hf_token image-name
   ```

### Sending Requests
Use `curl` to send audio files to the inference server:

#### Example Request
```sh
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: multipart/form-data" \
  -F "file=@les-conditions-du-tawhid-0_out_1.wav"
```

#### Windows Command Prompt Example
```sh
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: multipart/form-data" \
  -F "file=@C:\xamsadine-inference-server\les-conditions-du-tawhid-0_out_1.wav"
```

## Deployment
To deploy the inference server:
1. **Build and push the Docker image to a registry (e.g., Docker Hub, AWS ECR).**
2. **Deploy on a cloud service (e.g., AWS, Google Cloud, Digital Ocean).**

## License
This project is licensed under the MIT License.

## Contact
For any inquiries:
- **Email:** abdoullahaljersi@gmail.com
- **GitHub:** [utachicodes](https://github.com/utachicodes)

