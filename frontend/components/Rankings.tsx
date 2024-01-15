"use client";

import { ClockCountdown, WarningOctagon } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { Video as VideoModel } from "@/lib/video";
import { Video } from "./Video";

export function Rankings() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchRankings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function fetchRankings() {
    setLoading(true);
    client
      .getRankings()
      .then((response) => {
        console.log("Fetched videos: ", response.videos);
        setVideos(response.videos);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch videos: ", error);
        setLoading(false);
      });
  }

  function onClickVideo(video: VideoModel) {
    const url = `https://www.youtube.com/watch?v=${video.id}`;
  }

  return (
    <>
      {loading && (
        <div className="flex h-full flex-col items-center justify-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Loading</div>
          <ClockCountdown size={80} color="#3e8fda" />
        </div>
      )}

      {!loading && videos.length === 0 && (
        <div className="flex h-full flex-col items-center justify-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Failed to fetch videos</div>
          <WarningOctagon size={80} color="#f08080" />
        </div>
      )}

      {!loading && videos.length > 0 && (
        <div className="flex flex-wrap justify-center py-10">
          {videos.map((video, i) => (
            <Video
              key={i}
              video={video}
              onClick={onClickVideo}
              action="nothing"
              isCurrent={false}
            />
          ))}
        </div>
      )}
    </>
  );
}
