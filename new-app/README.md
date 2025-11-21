# MIB Alien Scanner App

Hyper-modern Vue.js app to scan aliens via the BodySafety agent.

## Prerequisites

- Node.js & npm
- BodySafety agent running (locally or deployed)

## Installation

```bash
cd new-app
npm install
```

## Configuration

If the agent is deployed on Google Cloud Agent Engine or elsewhere, update the API URL in the code (`src/App.vue`) or create a `.env.local` file:

```
VITE_AGENT_URL=https://your-agent-url/chat
```

By default, the app targets `http://localhost:8000/agent/chat` (via the Vite proxy in development).

## Run

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Architecture

- **App.vue**: Main orchestrator. Manages state (scan, loading, result).
- **CameraScanner.vue**: Handles camera access and image capture.
- **AgentResponse.vue**: Displays the agent's Markdown response with an MIB style.
- **Tailwind CSS**: Used for the "sexy", responsive design.

## Deployment (Cloud Run)

The app can be deployed as a static (Nginx) container on Cloud Run.

A deployment script is provided to make this easier:

```bash
./deploy_cloudrun.sh
```

This script:
1. Builds the Docker image (Node.js build + Nginx server).
2. Deploys to Cloud Run while injecting the backend agent URL via the `VITE_AGENT_URL` environment variable.

> **Configuration note**: Because this is a static application, environment variables are injected at container startup into a `config.js` file that is loaded by the browser. This lets you change the API URL without rebuilding the image.
