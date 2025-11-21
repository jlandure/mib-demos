# Le test en local

uv run adk web .

# Le test sur Agent Engine

uv run adk chat agent_engine \
    --project=jlandure-demos \
    --region=europe-west1 \
    --agent="MIB Bodysafety Agent"

# Le déploiement

uv run adk deploy agent_engine \
    --project=jlandure-demos \
    --region=europe-west1 \
    --staging_bucket=gs://jlandure-demos-mib-agent \
    --display_name="MIB Bodysafety Agent" \
    bodysafety

# Déploiement Cloud Run (Simple Server)

Se placer dans le dossier `bodysafety` :

```bash
cd bodysafety
gcloud run deploy mib-bodysafety-simple \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=jlandure-demos,GOOGLE_API_KEY=$GOOGLE_API_KEY
```
