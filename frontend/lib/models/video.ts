import { ThumbnailSet } from "@/lib/models/thumbnailSet";
import { VideoStats } from "@/lib/models/videoStats";

export type Video = {
  id: string;
  title: string;
  duration: string;
  channel_id: string;
  channel: string;
  published_at: string;
  thumbnails: ThumbnailSet;
  stats: VideoStats;
};
