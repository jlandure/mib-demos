# MIB BodySafety Agent

ADK agent capable of identifying aliens from uploaded photos and returning their characteristics from `data/data.yaml`.

## Prerequisites

### Install uv (ultra-fast Python package manager)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

> **Note:** `uv` will automatically install Python 3.13 and dependencies the first time you use it. No manual installation required.

## Configuration

The Gemini API key is loaded from the `.env` file at the root of the project.

If the file does not exist yet:

```bash
cd /Users/cubz/git/mib-mcp
echo 'GEMINI_API_KEY=your-gemini-api-key' > .env
```

Note: Internally, the key is converted to `GOOGLE_API_KEY` for ADK.

## Run

### Option 1: Automatic script (recommended)

```bash
./agents/python/bodysafety/run.sh
```

This script automatically loads the configuration and starts the web UI with uv.

### Option 2: Direct command with uv

```bash
cd agents/python/bodysafety
uv run adk web .
```

### Option 3: With environment variables

```bash
cd agents/python/bodysafety
export GEMINI_API_KEY="your-api-key"
export GOOGLE_API_KEY="$GEMINI_API_KEY"
uv run adk web .
```

### Option 4: Interactive CLI

```bash
cd agents/python/bodysafety
uv run adk run .
```

Open the displayed URL (usually `http://localhost:8000`), select the "bodysafety" agent, then upload an alien photo.

## How it works

1. The agent receives an image (Gemini multimodal).
2. It reads `data/data.yaml` through an MCP filesystem tool.
3. It identifies the alien and returns its characteristics (name, species, danger level, height, habitat, age, weight, photo, special notes).
4. If uncertain, it returns the top 3 candidates with their confidence level.

## Data

Alien data is in `/Users/cubz/git/mib-mcp/data/data.yaml`.
Images are in `/Users/cubz/git/mib-mcp/data/images/`.

