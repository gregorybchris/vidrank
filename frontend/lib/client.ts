import { Selection } from "./selection";
import { Video } from "./video";

export type GetVideosResponseBody = {
  videos: Video[];
};

export type PostSubmitRequestBody = {
  selection: Selection;
};

export type PostSubmitResponseBody = {
  record_id: string;
  videos: Video[];
};

export type PostUndoRequestBody = {
  record_id: string;
};

export type PostUndoResponseBody = {
  videos: Video[];
};

export type PostSkipRequestBody = {
  selection: Selection;
};

export type PostSkipResponseBody = {
  record_id: string;
  videos: Video[];
};

export type GetRankingsResponseBody = {
  videos: Video[];
};

export class Client {
  async getVideos(): Promise<GetVideosResponseBody> {
    const response = await fetch("http://localhost:8000/videos", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }

    return await response.json();
  }

  async postSubmit(selection: Selection): Promise<PostSubmitResponseBody> {
    const requestBody: PostSubmitRequestBody = { selection: selection };
    const response = await fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }

    return await response.json();
  }

  async postUndo(recordId: string): Promise<PostSkipResponseBody> {
    const requestBody: PostUndoRequestBody = { record_id: recordId };
    const response = await fetch("http://localhost:8000/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }

    return await response.json();
  }

  async postSkip(selection: Selection): Promise<PostSkipResponseBody> {
    const requestBody: PostSkipRequestBody = { selection: selection };
    const response = await fetch("http://localhost:8000/skip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }

    return await response.json();
  }

  async getRankings(): Promise<GetRankingsResponseBody> {
    const response = await fetch("http://localhost:8000/rankings", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }

    return await response.json();
  }
}
