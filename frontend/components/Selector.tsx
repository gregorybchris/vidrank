"use client";

import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { useKeyCombos } from "@/lib/keys";
import { Selection } from "@/lib/selection";
import { Video as VideoModel } from "@/lib/video";
import { match } from "ts-pattern";
import { Button } from "widgets/Button";
import { Video } from "./Video";

const MIN_SELECTED_VIDEOS = 2;
const MAX_SELECTED_VIDEOS = 4;
type Direction = "up" | "down" | "left" | "right";

export function Selector() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [removedIds, setRemovedIds] = useState<string[]>([]);
  const [currentId, setCurrentId] = useState<string>();

  useKeyCombos(
    [
      { pattern: "c", callback: () => clearActions() },
      { pattern: "u", callback: () => undoSubmit() },
      { pattern: "s", callback: () => skipVideoSet() },
      { pattern: "r", callback: () => removeCurrentVideo() },
      { pattern: "Enter", callback: () => submitVideoSet() },
      { pattern: "Escape", callback: () => setCurrentId(undefined) },
      { pattern: " ", callback: () => selectCurrentVideo() },
      { pattern: "ArrowUp", callback: () => offsetCurrentVideo("up") },
      { pattern: "ArrowDown", callback: () => offsetCurrentVideo("down") },
      { pattern: "ArrowLeft", callback: () => offsetCurrentVideo("left") },
      { pattern: "ArrowRight", callback: () => offsetCurrentVideo("right") },
    ],
    [videos, currentId, selectedIds, removedIds],
  );

  useEffect(() => {
    fetchVideos();
  }, []);

  function fetchVideos() {
    client.getVideos().then((videos) => {
      console.log("Fetched videos: ", videos);
      setVideos(videos);
      setSelectedIds([]);
      setRemovedIds([]);
      setCurrentId(undefined);
    });
  }

  function onClickVideo(video: VideoModel) {
    console.log(`Clicked video: ${video.title}`);
    selectVideo(video.id);
  }

  function skipVideoSet() {
    console.log("Will skip");
    client.postSkip().then((result) => {
      console.log("Got result: ", result);
      // TODO: Get new videos
    });
  }

  function undoSubmit() {
    console.log("Will undo");
    client.postUndo().then((result) => {
      console.log("Got result: ", result);
      // TODO: Get new videos
    });
  }

  function getVideoAction(video: VideoModel): Action {
    const selected = selectedIds.includes(video.id);
    const removed = removedIds.includes(video.id);

    return match([selected, removed])
      .with([true, true], (): Action => "remove")
      .with([true, false], (): Action => "select")
      .with([false, true], (): Action => "remove")
      .with([false, false], (): Action => "nothing")
      .exhaustive();
  }

  function submitVideoSet() {
    console.log("Will submit");
    const numActed = selectedIds.length + removedIds.length;

    if (numActed > MAX_SELECTED_VIDEOS) {
      console.log("Too many videos selected");
      // Use a toast to show this
      return;
    }
    if (numActed < MIN_SELECTED_VIDEOS) {
      console.log("Not enough videos selected");
      // Use a toast to show this
      return;
    }

    const selection: Selection = {
      videos: videos.map((video) => {
        return {
          video_id: video.id,
          action: getVideoAction(video),
        };
      }),
    };

    client.postSubmit(selection).then((result) => {
      console.log("Got result: ", result);
      // TODO: Get new videos
    });
  }
  ``;

  function selectVideo(videoId: string) {
    if (selectedIds.includes(videoId)) {
      setSelectedIds(selectedIds.filter((id) => id !== videoId));
    } else {
      if (removedIds.includes(videoId)) {
        setRemovedIds(removedIds.filter((id) => id !== videoId));
      }
      setSelectedIds([...selectedIds, videoId]);
    }
  }

  function removeVideo(videoId: string) {
    if (removedIds.includes(videoId)) {
      setRemovedIds(removedIds.filter((id) => id !== videoId));
    } else {
      if (selectedIds.includes(videoId)) {
        setSelectedIds(selectedIds.filter((id) => id !== videoId));
      }
      setRemovedIds([...removedIds, videoId]);
    }
  }

  function selectCurrentVideo() {
    console.log("Selecting current video");
    if (currentId === undefined) {
      return;
    }
    selectVideo(currentId);
  }

  function removeCurrentVideo() {
    console.log("Removing current video");
    if (currentId === undefined) {
      return;
    }
    removeVideo(currentId);
  }

  function clearActions() {
    console.log("Clearing actions");
    setSelectedIds([]);
    setRemovedIds([]);
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

    if (currentId === undefined) {
      console.log("No current video");
      setCurrentId(videos[0].id);
      return;
    }

    const currentIndex = videos.findIndex((video) => video.id === currentId);
    if (currentIndex == -1) {
      setCurrentId(videos[0].id);
      return;
    }

    let nextIndex = (currentIndex + offset + videos.length) % videos.length;
    setCurrentId(videos[nextIndex].id);
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
                action={getVideoAction(video)}
                isCurrent={!!currentId && video.id === currentId}
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

          <div className="flex w-full flex-row justify-center">
            <div className="w-[450px] border-t border-stone-900/20"></div>
          </div>
        </div>
      )}
    </>
  );
}
