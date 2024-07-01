# Vidrank

Use Vidrank to prioritize which YouTube videos to watch first. Vidrank presents you with small batches of videos. You can classify a subset of each batch as better than the rest and your selections are processed by the [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) algorithm to produce ratings. Ratings are used to determine the next best set of videos to consider to maximize information gain and decrease rating uncertainty.

If you have a backlog of videos waiting in your Watch Later playlist, then this tool was made for you.

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

Set a few environment variables that are used by the server.

> You will need an API key for the [YouTube Data API (v3)](https://developers.google.com/youtube/v3)

```bash
export YOUTUBE_API_KEY="<youtube-api-key>"
export VIDRANK_CACHE_DIR="<path-to-cache-directory>"
export VIDRANK_PLAYLIST_ID="<youtube-playlist-id>"
```

Start the backend

```bash
fastapi dev backend/vidrank/app/app.py --reload
```

Start the frontend

```bash
pnpm run dev
```

### Debug Mode

```bash
LOG_LEVEL=DEBUG fastapi dev backend/vidrank/app/app.py --reload
```
