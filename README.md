# Vidrank

Use Vidrank to prioritize which YouTube videos to watch first. You are presented with small batches of videos in a web interface. You must classify a subset of each batch as better than the rest. The results of your selections are processed by the [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) algorithm to produce an approximate ranking.

<div align="center">
    <img src="assets/main.png" width=500>
    <img src="assets/ratings.png" width=500>
</div>

## Installation

Requirements:

- [Node](https://nodejs.org/en/download)
- [Poetry](https://python-poetry.org/)

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
