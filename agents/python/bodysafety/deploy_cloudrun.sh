# Build & Deploy Script for MIB Agent on Cloud Run

# 0. Prepare data (local copy for Docker build context)
echo "Preparing data..."

# Load API key
ENV_FILE="../../../.env"
if [ -f "$ENV_FILE" ]; then
    echo "Loading secrets from $ENV_FILE..."
    export $(grep -v '^#' $ENV_FILE | xargs)
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "ERROR: API Key not found. Please create a .env file at the root of the project with GEMINI_API_KEY=..."
    echo "Or export GEMINI_API_KEY in your shell."
    exit 1
fi

# ADK uses GOOGLE_API_KEY, so make sure it is set
if [ -z "$GOOGLE_API_KEY" ]; then
    export GOOGLE_API_KEY="$GEMINI_API_KEY"
fi

mkdir -p data
# Copy from the mib-mcp/data folder at the project root into the local data/ folder
# Be careful with the relative path: the script lives in agents/python/bodysafety
cp -r ../../../data/data.yaml data/

# 1. Build the container image
echo "Building container..."
gcloud builds submit --tag gcr.io/jlandure-demos/mib-bodysafety-simple .

# 2. Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy mib-bodysafety-simple \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=jlandure-demos,GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --port 8080

