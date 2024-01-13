"use client";

import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { Video as VideoModel } from "@/lib/video";
import { Video } from "./Video";

export function Selector() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);

  useEffect(() => {
    fetchVideos();
  }, []);

  function fetchVideos() {
    client.getVideos().then((videos) => {
      setVideos(videos);
    });
  }

  function onClickVideo(video: VideoModel) {
    console.log(`Clicked video: ${video.title}`);
  }

  return (
    <div>
      {videos.length === 0 && <div>Loading videos...</div>}
      {videos.length > 0 && (
        <div className="grid grid-cols-2">
          {videos.map((video, i) => (
            <Video key={i} video={video} onClick={onClickVideo} />
          ))}
        </div>
      )}
    </div>
  );
}
