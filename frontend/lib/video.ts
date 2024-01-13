import { ThumbnailSet } from "@/lib/thumbnailSet";
import { VideoStats } from "./videoStats";

export type Video = {
  id: string;
  title: string;
  duration: number;
  channel: string;
  publish_datetime: string;
  thumbnails: ThumbnailSet;
  stats: VideoStats;
};
