import { CheckCircle, XCircle } from "@phosphor-icons/react";
/* eslint-disable @next/next/no-img-element */
import {
  formatDateDiff,
  formatDuration,
  formatNumberCompact,
} from "@/lib/formatUtilities";

import { cn } from "@/lib/styleUtilities";
import { getLargestThumbnail } from "@/lib/thumbnailSet";
import { Video as VideoModel } from "@/lib/video";
import styles from "@/styles/video.module.css";

type VideoProps = {
  className?: string;
  video: VideoModel;
  onClick: (video: VideoModel) => void;
  action: Action;
  isCurrent: boolean;
};

export function Video({
  className,
  video,
  onClick,
  action,
  isCurrent,
}: VideoProps) {
  const thumbnailUrl = getLargestThumbnail(video.thumbnails)?.url;
  const length = formatDuration(video.duration);

  return (
    <div
      className={cn("max-w-[300px]", className)}
      onClick={() => onClick(video)}
    >
      <div
        className={cn(
          "rounded-lg px-2 py-1 transition-all",
          isCurrent ? "bg-stone-300" : "bg-transparent",
        )}
      >
        <div className="cursor-pointer select-none ">
          <div className="flex flex-col items-start space-y-3 align-top">
            <div>
              {!thumbnailUrl && <div>No thumbnail found!</div>}
              {!!thumbnailUrl && (
                <div className="relative">
                  <img
                    className="h-[150px] w-[400px] rounded-lg object-cover"
                    src={thumbnailUrl}
                    alt="Video thumbnail"
                  />

                  <div className="align-center absolute bottom-2 right-2 rounded-md bg-stone-900/70 px-2 text-sm text-stone-200">
                    {length}
                  </div>

                  <div
                    className={cn(
                      "align-center absolute left-0 top-0 flex h-full w-full items-center justify-center rounded-md text-sm text-stone-200 transition-all",
                      action === "select" || action === "remove"
                        ? "bg-stone-900/70"
                        : "bg-stone-900/0 opacity-0",
                    )}
                  >
                    {action === "select" && (
                      <CheckCircle size={64} color="#80f080" />
                    )}
                    {action === "remove" && (
                      <XCircle size={64} color="#f08080" />
                    )}
                  </div>
                </div>
              )}
            </div>

            <div>
              <div className={cn("text-md", styles.videoTitle)}>
                {video.title}
              </div>
              <div className="truncate text-xs text-stone-500">
                {video.channel}
              </div>
              <div className="flex items-center space-x-1">
                <div className="text-xs text-stone-500">
                  {formatNumberCompact(video.stats.n_views)} views
                </div>
                <div>{"•"}</div>
                <div className="text-xs text-stone-500">
                  {formatDateDiff(video.publish_datetime)}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
