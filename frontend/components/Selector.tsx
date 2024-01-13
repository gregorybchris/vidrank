"use client";

import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { useKeyCombos } from "@/lib/keys";
import { Video as VideoModel } from "@/lib/video";
import { match } from "ts-pattern";
import { Button } from "widgets/Button";
import { Video } from "./Video";

type Direction = "up" | "down" | "left" | "right";

export function Selector() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [current, setCurrent] = useState<VideoModel>();

  useKeyCombos(
    [
      { pattern: "u", callback: () => undoSubmit() },
      { pattern: "s", callback: () => skipVideoSet() },
      { pattern: "Enter", callback: () => submitVideoSet() },
      { pattern: "Escape", callback: () => setCurrent(undefined) },
      { pattern: " ", callback: () => selectCurrentVideo() },
      { pattern: "ArrowUp", callback: () => offsetCurrentVideo("up") },
      { pattern: "ArrowDown", callback: () => offsetCurrentVideo("down") },
      { pattern: "ArrowLeft", callback: () => offsetCurrentVideo("left") },
      { pattern: "ArrowRight", callback: () => offsetCurrentVideo("right") },
    ],
    [videos, current, selected],
  );

  useEffect(() => {
    fetchVideos();
  }, []);

  function fetchVideos() {
    client.getVideos().then((videos) => {
      console.log("Fetched videos: ", videos);
      setVideos(videos);
      setSelected([]);
      setCurrent(undefined);
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

  function skipVideoSet() {
    console.log("Will skip");
  }

  function undoSubmit() {
    console.log("Will undo");
  }

  function submitVideoSet() {
    console.log("Will submit");
  }

  function selectCurrentVideo() {
    console.log("Selecting current video");
    if (current === undefined) {
      return;
    }

    if (selected.includes(current.id)) {
      setSelected(selected.filter((id) => id !== current.id));
    } else {
      setSelected([...selected, current.id]);
    }
  }

  function offsetCurrentVideo(direction: Direction) {
    console.log("Offsetting current video: ", direction);
    const offset = match(direction)
      .with("up", () => -1)
      .with("down", () => 1)
      .with("left", () => -1)
      .with("right", () => 1)
      .exhaustive();

    if (videos.length === 0) {
      console.log("No videos");
      return;
    }

    if (current === undefined) {
      console.log("No current video");
      setCurrent(videos[0]);
      return;
    }

    const currentIndex = videos.findIndex((video) => video.id === current.id);
    if (currentIndex == -1) {
      setCurrent(videos[0]);
      return;
    }

    let nextIndex = (currentIndex + offset + videos.length) % videos.length;
    setCurrent(videos[nextIndex]);
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
                isCurrent={!!current && video.id === current.id}
              />
            ))}
          </div>

          <div className="flex w-full flex-row justify-center">
            <div className="w-[450px] border-t border-stone-900/20"></div>
          </div>

          <div className="flex flex-row justify-center space-x-2">
            <Button text="Skip" onClick={skipVideoSet} />
            <Button text="Undo" onClick={undoSubmit} />
            <Button text="Submit" onClick={submitVideoSet} />
          </div>
        </div>
      )}
    </>
  );
}
