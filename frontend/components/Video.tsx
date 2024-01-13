import { formatDateDiff, formatDuration, formatNumberCompact } from "@/lib/formatUtilities";

import { cn } from "@/lib/styleUtilities";
import { getLargestThumbnail } from "@/lib/thumbnailSet";
import { Video as VideoModel } from "@/lib/video";
import styles from "@/styles/video.module.css";

type VideoProps = {
  className?: string;
  video: VideoModel;
  onClick: (video: VideoModel) => void;
};

export function Video({ className, video, onClick }: VideoProps) {
  return (
    <div className={cn("max-w-[300px]", className)} onClick={() => onClick(video)}>
      <div className="px-4 py-2">
        <div className="flex flex-col items-start space-y-3 align-top">
          <Thumbnail video={video} />

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

function Thumbnail(props: { video: VideoModel }) {
  const url = getLargestThumbnail(props.video.thumbnails)?.url;
  const length = formatDuration(props.video.duration);
  return (
    <div>
      {!url && <div>No thumbnail found!</div>}
      {!!url && (
        <div className="relative">
          {/* <img class="object-cover h-48 w-96 ..."> */}
          {/* <Image className="rounded-lg" src={url} alt="Video thumbnail" height={200} width={300} /> */}
          <img className="object-cover h-[150px] w-[400px] rounded-lg" src={url} />
          <div className="text-sm absolute bottom-2 align-center right-2 bg-neutral-900/70 text-neutral-200 px-2 rounded-md">
            {length}
          </div>
        </div>
      )}
    </div>
  );
}
