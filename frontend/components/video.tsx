/* eslint-disable @next/next/no-img-element */
import {
  formatDateDiff,
  formatDuration,
  formatNumberCompact,
} from "@/lib/utilities/format-utilities";
import {
  CheckCircle,
  Clipboard,
  LinkSimpleHorizontal,
  XCircle,
} from "@phosphor-icons/react";

import { getLargestThumbnail } from "@/lib/models/thumbnail-set";
import { Video as VideoModel } from "@/lib/models/video";
import { cn } from "@/lib/utilities/style-utilities";
import {
  urlFromChannelId,
  urlFromVideoId,
} from "@/lib/utilities/url-utilities";
import styles from "@/styles/video.module.css";
import Link from "next/link";

type VideoProps = {
  className?: string;
  video: VideoModel;
  onClick: (video: VideoModel) => void;
  action: Action;
  isCurrent: boolean;
  rating?: number;
};

export function Video({
  className,
  video,
  onClick,
  action,
  isCurrent,
  rating,
}: VideoProps) {
  return (
    <div className={cn("w-[300px]", className)} onClick={() => onClick(video)}>
      <div
        className={cn(
          "rounded-lg p-2 transition-all",
          isCurrent ? "bg-stone-300" : "bg-transparent",
        )}
      >
        <div className="group select-none">
          <div className="flex flex-col items-start gap-3 align-top">
            <VideoThumbnail video={video} action={action} rating={rating} />
            <VideoDetails video={video} />
          </div>
        </div>
      </div>
    </div>
  );
}

type VideoThumbnailProps = {
  className?: string;
  video: VideoModel;
  action: Action;
  rating?: number;
};

function VideoThumbnail({
  className,
  video,
  action,
  rating,
}: VideoThumbnailProps) {
  const thumbnailUrl = getLargestThumbnail(video.thumbnails)?.url;
  const length = formatDuration(video.duration);

  return (
    <div className={cn("", className)}>
      {!thumbnailUrl && <div>No thumbnail found!</div>}
      {!!thumbnailUrl && (
        <div className="relative">
          <img
            className="h-[160px] w-[400px] rounded-lg object-cover"
            src={thumbnailUrl}
            alt="Video thumbnail"
          />

          {rating && (
            <div className="absolute right-2 top-2 flex h-8 w-8 flex-col items-center justify-center rounded-full bg-stone-900/70 text-center text-sm text-stone-100">
              {Math.round(rating)}
            </div>
          )}

          <div className="absolute bottom-2 right-2 rounded-md bg-stone-900/70 px-2 text-sm text-stone-100">
            {length}
          </div>

          <div
            className={cn(
              "absolute left-0 top-0 flex h-full w-full items-center justify-center rounded-md text-sm text-stone-200 transition-all",
              action === "select" || action === "remove"
                ? "bg-stone-900/70"
                : "bg-stone-900/0 opacity-0",
            )}
          >
            {action === "select" && <CheckCircle size={64} color="#80f080" />}
            {action === "remove" && <XCircle size={64} color="#f08080" />}
          </div>
        </div>
      )}
    </div>
  );
}

type VideoDetailsProps = {
  className?: string;
  video: VideoModel;
};

function VideoDetails({ className, video }: VideoDetailsProps) {
  return (
    <div className={cn("", className)}>
      <div className={cn("text-md", styles.videoTitle)}>{video.title}</div>
      <Link href={urlFromChannelId(video.channel_id)} target="_blank">
        <div className="inline-block truncate text-xs text-stone-500 transition-all hover:text-stone-800">
          {video.channel}
        </div>
      </Link>

      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1">
          <div className="text-xs text-stone-500">
            {formatNumberCompact(video.stats.n_views)} views
          </div>
          <div>{"•"}</div>
          <div className="text-xs text-stone-500">
            {formatDateDiff(video.published_at)}
          </div>
        </div>

        <Link
          href={urlFromVideoId(video.id)}
          target="_blank"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col items-center justify-center rounded-md bg-stone-900/10 px-2 py-1 text-sm text-stone-200 transition-all hover:bg-stone-900/20 active:bg-stone-900/30">
            <LinkSimpleHorizontal size={16} color="#404040" />
          </div>
        </Link>

        <div
          className="flex cursor-pointer flex-col items-center justify-center rounded-md bg-stone-900/10 px-2 py-1 text-sm text-stone-200 transition-all hover:bg-stone-900/20 active:bg-stone-900/30"
          onClick={(e) => {
            navigator.clipboard.writeText(video.id);
            e.stopPropagation();
          }}
        >
          <Clipboard size={16} color="#404040" />
        </div>
      </div>
    </div>
  );
}
