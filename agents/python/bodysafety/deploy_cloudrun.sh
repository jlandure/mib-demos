# Build & Deploy Script for MIB Agent on Cloud Run

# 0. Préparation des données (copie locale pour le build Docker context)
echo "Preparing data..."

# Récupération de la clé API
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

# ADK utilise GOOGLE_API_KEY, donc on s'assure qu'elle est définie
if [ -z "$GOOGLE_API_KEY" ]; then
    export GOOGLE_API_KEY="$GEMINI_API_KEY"
fi

mkdir -p data
# On copie depuis la racine du projet mib-mcp/data vers le dossier courant data/
# Attention au chemin relatif : le script est dans agents/python/bodysafety
cp -r ../../../data/data.yaml data/

# 1. Build de l'image
echo "Building container..."
gcloud builds submit --tag gcr.io/jlandure-demos/mib-bodysafety-simple .

# 2. Déploiement sur Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy mib-bodysafety-simple \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=jlandure-demos,GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --port 8080

