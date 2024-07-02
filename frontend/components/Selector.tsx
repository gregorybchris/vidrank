"use client";

import { ClockCountdown, WarningOctagon } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Video } from "@/components/Video";
import { Client } from "@/lib/client";
import { useKeyCombos } from "@/lib/hooks/keys";
import { useSettings } from "@/lib/hooks/settings";
import { ChoiceSet } from "@/lib/models/choiceSet";
import { Video as VideoModel } from "@/lib/models/video";
import { match } from "ts-pattern";
import { Button } from "widgets/Button";
import { Toast } from "widgets/Toast";

type Direction = "up" | "down" | "left" | "right";
type SubmitStatus = { canSubmit: boolean; message: string };

export function Selector() {
  const client = new Client();
  const [videos, setVideos] = useState<VideoModel[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [removedIds, setRemovedIds] = useState<string[]>([]);
  const [currentId, setCurrentId] = useState<string>();
  const [recordIds, setRecordIds] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [toastVisible, setToastVisible] = useState<boolean>(false);
  const [toastDescription, setToastDescription] = useState<string>("");
  const [settings] = useSettings();

  const keys = useKeyCombos(
    [
      { pattern: "c", callback: () => clearActions() },
      { pattern: "u", callback: () => undoSubmit() },
      { pattern: "s", callback: () => skipVideoSet() },
      { pattern: "r", callback: () => {} },
      { pattern: "Enter", callback: () => submitVideoSet() },
      { pattern: "Escape", callback: () => setCurrentId(undefined) },
      { pattern: " ", callback: () => updateCurrentVideoAction() },
      { pattern: "r+ ", callback: () => updateCurrentVideoAction() },
      { pattern: "ArrowUp", callback: () => offsetCurrentVideo("up") },
      { pattern: "ArrowDown", callback: () => offsetCurrentVideo("down") },
      { pattern: "ArrowLeft", callback: () => offsetCurrentVideo("left") },
      { pattern: "ArrowRight", callback: () => offsetCurrentVideo("right") },
    ],
    [videos, currentId, selectedIds, removedIds],
  );

  useEffect(() => {
    if (settings !== null) {
      fetchVideos();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [settings]);

  function fetchVideos() {
    if (settings === null) {
      console.error("Settings have not loaded yet");
      return;
    }

    setLoading(true);
    client
      .postVideos(settings)
      .then((response) => {
        console.log("Fetched videos: ", response.videos);
        updateWithVideos(response.videos);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch videos: ", error);
        setLoading(false);
      });
  }

  function updateWithVideos(videos: VideoModel[]) {
    setVideos(videos);
    setSelectedIds([]);
    setRemovedIds([]);
    setCurrentId(undefined);
  }

  function onClickVideo(video: VideoModel) {
    console.log(`Clicked video: ${video.title}`);
    updateVideoAction(video);
  }

  function getSubmitStatus(): SubmitStatus {
    const MIN_ACTIONS = 1;
    const MAX_SELECTIONS = 4;

    const numActions = selectedIds.length + removedIds.length;
    const numSelected = selectedIds.length;
    const numNothing = videos.length - numActions;

    if (numSelected > MAX_SELECTIONS) {
      return {
        canSubmit: false,
        message: `Select at most ${MAX_SELECTIONS} videos`,
      };
    }
    if (numActions < MIN_ACTIONS) {
      return {
        canSubmit: false,
        message: `Perform at least ${MIN_ACTIONS} action`,
      };
    }
    if (numSelected > 0 && numNothing == 0) {
      return { canSubmit: false, message: "Must have some videos unselected" };
    }
    return { canSubmit: true, message: "Ready to submit" };
  }

  function canSubmit(): boolean {
    const { canSubmit } = getSubmitStatus();
    return canSubmit;
  }

  function submitVideoSet() {
    console.log("Will submit");

    if (settings === null) {
      console.error("Settings have not loaded yet");
      return;
    }

    const choiceSet: ChoiceSet = {
      choices: videos.map((video) => {
        return {
          video_id: video.id,
          action: getVideoAction(video),
        };
      }),
    };

    setLoading(true);
    client
      .postSubmit(choiceSet, settings)
      .then((response) => {
        console.log("Submit successful: ", response.record_id);
        setRecordIds([...recordIds, response.record_id]);
        updateWithVideos(response.videos);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to submit: ", error);
        setLoading(false);
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

  function undoSubmit() {
    console.log("Will undo");
    if (recordIds.length === 0) {
      console.warn("No records to undo");
      return;
    }
    const recordId = recordIds[recordIds.length - 1];
    setLoading(true);
    client
      .postUndo(recordId)
      .then((response) => {
        console.log("Got videos: ", response.videos);
        updateWithVideos(response.videos);
        setRecordIds(recordIds.slice(0, recordIds.length - 1));
        const choices = response.choice_set.choices;
        setSelectedIds(
          choices.filter((c) => c.action == "select").map((c) => c.video_id),
        );
        setRemovedIds(
          choices.filter((c) => c.action == "remove").map((c) => c.video_id),
        );
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to undo: ", error);
        setLoading(false);
      });
  }

  function skipVideoSet() {
    console.log("Will skip");

    if (settings === null) {
      console.error("Settings have not loaded yet");
      return;
    }

    const choiceSet: ChoiceSet = {
      choices: videos.map((video) => {
        return {
          video_id: video.id,
          action: "nothing",
        };
      }),
    };

    setLoading(true);
    client
      .postSkip(choiceSet, settings)
      .then((response) => {
        console.log("Got videos: ", response.videos);
        setRecordIds([...recordIds, response.record_id]);
        updateWithVideos(response.videos);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to skip: ", error);
        setLoading(false);
      });
  }

  function setVideoAction(videoId: string, action: Action) {
    setSelectedIds(selectedIds.filter((id) => id !== videoId));
    setRemovedIds(removedIds.filter((id) => id !== videoId));

    if (action === "select") {
      setSelectedIds([...selectedIds, videoId]);
    } else if (action === "remove") {
      setRemovedIds([...removedIds, videoId]);
    }
  }

  function updateVideoAction(video: VideoModel) {
    const action = getVideoAction(video);

    if (keys.includes("r")) {
      setVideoAction(video.id, "remove");
    } else {
      if (action === "select" || action === "remove") {
        setVideoAction(video.id, "nothing");
      } else {
        setVideoAction(video.id, "select");
      }
    }
  }

  function updateCurrentVideoAction() {
    console.log("Selecting/deselecting current video");
    if (currentId === undefined) {
      return;
    }

    const currentVideo = videos.find((video) => video.id === currentId);
    if (currentVideo === undefined) {
      return;
    }

    updateVideoAction(currentVideo);
  }

  function clearActions() {
    console.log("Clearing actions");
    setSelectedIds([]);
    setRemovedIds([]);
  }

  function offsetCurrentVideo(direction: Direction) {
    console.log("Offsetting current video: ", direction);

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

    const verticalOffset = 3; // nVideos / nRows = nCols = 3
    const offset = match(direction)
      .with("up", () => -verticalOffset)
      .with("down", () => verticalOffset)
      .with("left", () => -1)
      .with("right", () => 1)
      .exhaustive();

    let nextIndex = (currentIndex + offset + videos.length) % videos.length;
    setCurrentId(videos[nextIndex].id);
  }

  return (
    <>
      {loading && (
        <div className="flex flex-col items-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Loading</div>
          <ClockCountdown size={80} color="#3e8fda" />
        </div>
      )}

      {!loading && videos.length === 0 && (
        <div className="flex flex-col items-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Failed to fetch videos</div>
          <WarningOctagon size={80} color="#f08080" />
        </div>
      )}

      {!loading && videos.length > 0 && (
        <div className="flex flex-col justify-center space-y-10 lg:px-[150px]">
          <div className="flex flex-wrap justify-center">
            {videos.map((video, i) => (
              <div key={i} className="cursor-pointer">
                <Video
                  video={video}
                  onClick={onClickVideo}
                  action={getVideoAction(video)}
                  isCurrent={!!currentId && video.id === currentId}
                />
              </div>
            ))}
          </div>

          <div className="flex flex-col justify-center space-y-3">
            <div className="flex w-full flex-row justify-center">
              <div className="w-[450px] border-t border-stone-900/20"></div>
            </div>

            <div className="flex flex-row justify-center space-x-2">
              <Button text="Skip" onClick={skipVideoSet} />
              <Button
                text="Undo"
                onClick={undoSubmit}
                enabled={recordIds.length > 0}
                onClickDisabled={() => {
                  setToastDescription("Nothing to undo");
                  setToastVisible(true);
                }}
              />
              <Button
                text="Submit"
                onClick={submitVideoSet}
                enabled={canSubmit()}
                onClickDisabled={() => {
                  const { message } = getSubmitStatus();
                  setToastDescription(message);
                  setToastVisible(true);
                }}
              />
            </div>

            <div className="flex w-full flex-row justify-center">
              <div className="w-[450px] border-t border-stone-900/20"></div>
            </div>
          </div>
        </div>
      )}

      <Toast
        visible={toastVisible}
        setVisible={setToastVisible}
        title="Cannot submit"
        description={toastDescription}
        buttonText="Ok"
      />
    </>
  );
}
