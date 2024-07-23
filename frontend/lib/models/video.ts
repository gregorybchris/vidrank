import { ThumbnailSet } from "@/lib/models/thumbnail-set";
import { VideoStats } from "@/lib/models/video-stats";

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
