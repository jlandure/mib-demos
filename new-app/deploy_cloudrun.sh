#!/bin/bash

# URL of the backend agent
AGENT_URL="https://mib-bodysafety-simple-347864781165.europe-west1.run.app/agent/chat"

echo "Deploying new-app to Cloud Run..."

gcloud run deploy mib-new-app \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars VITE_AGENT_URL=$AGENT_URL

