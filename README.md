# Vidrank

Tool for ranking YouTube videos in large playlists.

## Installation

Requirements:

- Node
- Poetry

Install the backend package

```bash
cd backend
poetry install
```

Install the frontend package

```bash
cd frontend
pnpm install
```

## Running locally

Set a few environment variables that are used by the server

```bash
export YOUTUBE_API_KEY="<youtube-api-key>"
export VIDRANK_CACHE_DIR="<path-to-cache-directory>"
export VIDRANK_PLAYLIST_ID="<youtube-playlist-id>"
```

Start the backend

```bash
vidrank serve
```

Start the frontend

```bash
pnpm run dev
```
