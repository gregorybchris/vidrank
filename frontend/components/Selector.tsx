"use client";

import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { Video as VideoModel } from "@/lib/video";
import { Button } from "widgets/Button";
import { Video } from "./Video";

export function Selector() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);
  const [selected, setSelected] = useState<string[]>([]);

  useEffect(() => {
    fetchVideos();
  }, []);

  function fetchVideos() {
    client.getVideos().then((videos) => {
      console.log("got videos: ", videos);
      setVideos(videos);
      setSelected([]);
    });
  }

  function onClickVideo(video: VideoModel) {
    console.log(`Clicked video: ${video.title}`);
    if (selected.includes(video.id)) {
      setSelected(selected.filter((id) => id !== video.id));
    } else {
      setSelected([...selected, video.id]);
    }
  }

  function onClickSubmit() {
    console.log("Will submit");
  }

  function onClickUndo() {
    console.log("Will undo");
  }

  function onClickSkip() {
    console.log("Will skip");
  }

  return (
    <>
      {videos.length === 0 && <div>Loading videos...</div>}
      {videos.length > 0 && (
        <div className="flex flex-col justify-center space-y-4">
          <div className="flex flex-wrap justify-center">
            {videos.map((video, i) => (
              <Video
                key={i}
                video={video}
                onClick={onClickVideo}
                isSelected={selected.includes(video.id)}
              />
            ))}
          </div>

          <div className="flex w-full flex-row justify-center">
            <div className="w-[450px] border-t border-stone-900/20"></div>
          </div>

          <div className="flex flex-row justify-center space-x-5">
            <Button text="Skip" onClick={onClickSkip} />
            <Button text="Undo" onClick={onClickUndo} />
            <Button text="Submit" onClick={onClickSubmit} />
          </div>
        </div>
      )}
    </>
  );
}
