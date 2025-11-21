# Local testing

uv run adk web .

# Testing on Agent Engine

uv run adk chat agent_engine \
    --project=jlandure-demos \
    --region=europe-west1 \
    --agent="MIB Bodysafety Agent"

# Deployment

uv run adk deploy agent_engine \
    --project=jlandure-demos \
    --region=europe-west1 \
    --staging_bucket=gs://jlandure-demos-mib-agent \
    --display_name="MIB Bodysafety Agent" \
    bodysafety

# Cloud Run deployment (simple server)

From the `bodysafety` folder:

```bash
cd bodysafety
gcloud run deploy mib-bodysafety-simple \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=jlandure-demos,GOOGLE_API_KEY=$GOOGLE_API_KEY
```
