import { formatDateDiff, formatDuration, formatNumberCompact } from "@/lib/formatUtilities";

import { cn } from "@/lib/styleUtilities";
import { getLargestThumbnail } from "@/lib/thumbnailSet";
import { Video as VideoModel } from "@/lib/video";
import styles from "@/styles/video.module.css";
import { CheckCircle } from "@phosphor-icons/react";

type VideoProps = {
  className?: string;
  video: VideoModel;
  onClick: (video: VideoModel) => void;
  isSelected: boolean;
};

export function Video({ className, video, onClick, isSelected }: VideoProps) {
  const thumbnailUrl = getLargestThumbnail(video.thumbnails)?.url;
  const length = formatDuration(video.duration);

  return (
    <div className={cn("max-w-[300px]", className)} onClick={() => onClick(video)}>
      <div className="px-4 py-2 select-none">
        <div className="flex flex-col items-start space-y-3 align-top">
          <div>
            {!thumbnailUrl && <div>No thumbnail found!</div>}
            {!!thumbnailUrl && (
              <div className="relative cursor-pointer">
                {/* <Image className="rounded-lg" src={url} alt="Video thumbnail" height={200} width={300} /> */}
                <img className="opacity object-cover h-[150px] w-[400px] rounded-lg" src={thumbnailUrl} />
                <div className="text-sm absolute bottom-2 align-center right-2 bg-neutral-900/70 text-neutral-200 px-2 rounded-md">
                  {length}
                </div>

                <div
                  className={cn(
                    "text-sm absolute top-0 align-center flex items-center justify-center left-0 text-neutral-200 w-full h-full rounded-md transition-all",
                    isSelected ? "bg-neutral-900/70" : "bg-neutral-900/0 opacity-0"
                  )}
                >
                  <CheckCircle size={64} color="#e0e0e0" />
                </div>
              </div>
            )}
          </div>

          <div>
            <div className={cn("text-md", styles.videoTitle)}>{video.title}</div>
            <div className="text-xs text-neutral-500 truncate">{video.channel}</div>
            <div className="flex space-x-1 items-center">
              <div className="text-xs text-neutral-500">{formatNumberCompact(video.stats.n_views)} views</div>
              <div>{"•"}</div>
              <div className="text-xs text-neutral-500">{formatDateDiff(video.publish_datetime)}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
