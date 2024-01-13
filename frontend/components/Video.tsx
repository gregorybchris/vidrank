import { formatNumberCompact } from "@/lib/formatUtilities";
import { cn } from "@/lib/styleUtilities";
import { getLargestThumbnail } from "@/lib/thumbnailSet";
import { Video as VideoModel } from "@/lib/video";
import styles from "@/styles/video.module.css";
import Image from "next/image";

type VideoProps = {
  className?: string;
  video: VideoModel;
  onClick: (video: VideoModel) => void;
};

export function Video({ className, video, onClick }: VideoProps) {
  return (
    <div className={cn("", className)} onClick={() => onClick(video)}>
      <div className="px-4 py-2 transition-all">
        <div className="flex items-start space-x-5 align-top">
          <div className="w-48 shrink-0">
            <Thumbnail video={video} />
          </div>

          <div>
            <div className={cn("text-lg", styles.videoTitle)}>{video.title}</div>
            <div className="inline-block truncate transition-all">{video.channel}</div>
            {/* <div className="">{formatDateDiff(video.publish_datetime)}</div> */}
            <div>{formatNumberCompact(video.stats.n_views)} views</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Thumbnail(props: { video: VideoModel }) {
  const url = getLargestThumbnail(props.video.thumbnails)?.url;
  // const length = formatDuration(props.video.length);
  return (
    <div>
      {!url && <div>No thumbnail found!</div>}
      {!!url && (
        <div className="relative">
          <Image className="rounded-lg" src={url} alt="Video thumbnail" height={200} width={300} />
          {/* <img className="rounded-xl" src={url} /> */}
          {/* <div className="absolute bottom-2 right-2 bg-zinc-900 px-2 rounded-md">{length}</div> */}
        </div>
      )}
    </div>
  );
}
