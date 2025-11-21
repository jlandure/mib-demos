# MIB Alien Scanner App

App Vue.js "hyper moderne" pour scanner les aliens via l'agent BodySafety.

## Prérequis

- Node.js & npm
- L'agent BodySafety qui tourne (localement ou déployé)

## Installation

```bash
cd new-app
npm install
```

## Configuration

Si l'agent est déployé sur Google Cloud Agent Engine ou ailleurs, modifiez l'URL de l'API dans le code (`src/App.vue`) ou créez un fichier `.env.local` :

```
VITE_AGENT_URL=https://votre-agent-url/chat
```

Par défaut, l'application tape sur `http://localhost:8000/agent/chat` (via le proxy Vite pour le développement).

## Lancement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`.

## Architecture

- **App.vue** : Orchestrateur principal. Gère l'état (scan, chargement, résultat).
- **CameraScanner.vue** : Gère l'accès caméra et la capture d'image.
- **AgentResponse.vue** : Affiche la réponse Markdown de l'agent avec un style MIB.
- **Tailwind CSS** : Utilisé pour le design "sexy" et réactif.
