# MIB BodySafety Agent

Agent ADK capable d'identifier des aliens à partir de photos uploadées et de retourner leurs caractéristiques depuis `data/data.yaml`.

## Prérequis

### Installer uv (gestionnaire de packages Python ultra-rapide)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou avec Homebrew
brew install uv
```

> **Note :** `uv` installera automatiquement Python 3.13 et les dépendances lors de la première utilisation. Pas besoin d'installation manuelle !

## Configuration

La clé API Gemini est chargée depuis le fichier `.env` à la racine du projet.

Si le fichier n'existe pas encore :

```bash
cd /Users/cubz/git/mib-mcp
echo 'GEMINI_API_KEY=your-gemini-api-key' > .env
```

Note : En interne, la clé est convertie en `GOOGLE_API_KEY` pour ADK.

## Lancement

### Option 1 : Script automatique (recommandé)

```bash
./agents/python/bodysafety/run.sh
```

Ce script charge automatiquement la configuration et lance l'UI web avec uv.

### Option 2 : Commande directe avec uv

```bash
cd agents/python/bodysafety
uv run adk web .
```

### Option 3 : Avec variables d'environnement

```bash
cd agents/python/bodysafety
export GEMINI_API_KEY="ta-clé-api"
export GOOGLE_API_KEY="$GEMINI_API_KEY"
uv run adk web .
```

### Option 4 : CLI interactif

```bash
cd agents/python/bodysafety
uv run adk run .
```

Ouvre l'URL affichée (généralement `http://localhost:8000`), sélectionne l'agent "bodysafety", puis upload une photo d'alien.

## Fonctionnement

1. L'agent reçoit une image (multimodal Gemini).
2. Il lit `data/data.yaml` via un outil MCP filesystem.
3. Il identifie l'alien et retourne ses caractéristiques (nom, espèce, dangerosité, taille, habitat, âge, poids, photo, notes spéciales).
4. Si incertain, il retourne le top 3 des candidats avec leur niveau de confiance.

## Données

Les données des aliens sont dans `/Users/cubz/git/mib-mcp/data/data.yaml`.
Les photos sont dans `/Users/cubz/git/mib-mcp/data/images/`.

