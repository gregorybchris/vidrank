import { Selection } from "./selection";
import { Video } from "./video";

export type GetVideosResponseBody = {
  videos: Video[];
};

export type PostSkipResponseBody = {
  result: string;
};

export type PostUndoResponseBody = {
  result: string;
};

export type PostSubmitResponseBody = {
  result: string;
};

export class Client {
  async getVideos(): Promise<Video[]> {
    const response = await fetch("http://localhost:8000/videos", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status !== 200) {
      const { error } = await response.json();
      console.error(error);
      throw Error(error);
    }

    const { videos }: GetVideosResponseBody = await response.json();
    return videos;
  }

  async postSkip(): Promise<string> {
    const response = await fetch("http://localhost:8000/skip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status !== 200) {
      const { error } = await response.json();
      console.error(error);
      throw Error(error);
    }

    const { result }: PostSkipResponseBody = await response.json();
    return result;
  }

  async postUndo(): Promise<string> {
    const response = await fetch("http://localhost:8000/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status !== 200) {
      const { error } = await response.json();
      console.error(error);
      throw Error(error);
    }

    const { result }: PostUndoResponseBody = await response.json();
    return result;
  }

  async postSubmit(selection: Selection): Promise<string> {
    console.log(JSON.stringify(selection));
    const response = await fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(selection),
    });

    if (response.status !== 200) {
      const { error } = await response.json();
      console.error(error);
      throw Error(error);
    }

    const { result }: PostSubmitResponseBody = await response.json();
    return result;
  }
}
