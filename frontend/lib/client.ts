import { ChoiceSet } from "@/lib/models/choiceSet";
import { Ranking } from "@/lib/models/ranking";
import { Settings } from "@/lib/models/settings";
import { Video } from "@/lib/models/video";

export type PostVideosRequestBody = {
  settings: Settings;
};

export type PostVideosResponseBody = {
  videos: Video[];
};

export type PostSubmitRequestBody = {
  choice_set: ChoiceSet;
  settings: Settings;
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
  choice_set: ChoiceSet;
};

export type PostSkipRequestBody = {
  choice_set: ChoiceSet;
  settings: Settings;
};

export type PostSkipResponseBody = {
  record_id: string;
  videos: Video[];
};

export type GetRankingsResponseBody = {
  rankings: Ranking[];
};

export class Client {
  async postVideos(settings: Settings): Promise<PostVideosResponseBody> {
    console.log("Posting videos with settings", settings);
    const requestBody: PostVideosRequestBody = { settings: settings };
    const response = await fetch("http://localhost:8000/videos?", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postSubmit(
    choiceSet: ChoiceSet,
    settings: Settings,
  ): Promise<PostSubmitResponseBody> {
    const requestBody: PostSubmitRequestBody = {
      choice_set: choiceSet,
      settings: settings,
    };
    const response = await fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postUndo(recordId: string): Promise<PostUndoResponseBody> {
    const requestBody: PostUndoRequestBody = { record_id: recordId };
    const response = await fetch("http://localhost:8000/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postSkip(
    choiceSet: ChoiceSet,
    settings: Settings,
  ): Promise<PostSkipResponseBody> {
    const requestBody: PostSkipRequestBody = {
      choice_set: choiceSet,
      settings: settings,
    };
    const response = await fetch("http://localhost:8000/skip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async getRankings(): Promise<GetRankingsResponseBody> {
    const response = await fetch("http://localhost:8000/rankings", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async throwOnError(response: Response): Promise<void> {
    if (response.status !== 200) {
      const responseJson = await response.json();
      console.error(responseJson);
      throw Error(JSON.stringify(responseJson));
    }
  }
}
