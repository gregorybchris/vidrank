export function urlFromVideoId(videoId: string): string {
  return `https://www.youtube.com/watch?v=${videoId}`;
}

export function urlFromChannelId(channelId: string): string {
  return `https://www.youtube.com/channel/${channelId}`;
}

export function urlFromPlaylistId(playlistId: string): string {
  return `https://www.youtube.com/playlist?list=${playlistId}`;
}
