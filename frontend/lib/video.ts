import { ThumbnailSet } from "@/lib/thumbnailSet";
import { VideoStats } from "./videoStats";

export type Video = {
  id: string;
  title: string;
  duration: number;
  channel: string;
  publish_datetime: number;
  thumbnails: ThumbnailSet;
  stats: VideoStats;
};
