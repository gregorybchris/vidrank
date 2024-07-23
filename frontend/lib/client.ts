import { ChoiceSet } from "@/lib/models/choice-set";
import { Ranking } from "@/lib/models/ranking";
import { Settings } from "@/lib/models/settings";
import { Video } from "@/lib/models/video";

export type PostVideosRequest = {
  settings: Settings;
};

export type PostVideosResponse = {
  videos: Video[];
};

export type PostSubmitRequest = {
  choice_set: ChoiceSet;
  settings: Settings;
};

export type PostSubmitResponse = {
  record_id: string;
  videos: Video[];
};

export type PostUndoRequest = {
  record_id: string;
};

export type PostUndoResponse = {
  videos: Video[];
  choice_set: ChoiceSet;
};

export type PostSkipRequest = {
  choice_set: ChoiceSet;
  settings: Settings;
};

export type PostSkipResponse = {
  record_id: string;
  videos: Video[];
};

export type PostRankingsRequest = {
  page_number: number;
  page_size: number;
};

export type PostRankingsResponse = {
  n_pages: number;
  page_number: number;
  rankings_page: Ranking[];
};

export class Client {
  apiBaseUrl: string;

  constructor() {
    if (process.env.NEXT_PUBLIC_API_BASE_URL === undefined) {
      console.error("NEXT_PUBLIC_API_BASE_URL is not set");
    }
    this.apiBaseUrl =
      process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
  }

  async postVideos(settings: Settings): Promise<PostVideosResponse> {
    const requestBody: PostVideosRequest = { settings: settings };
    return await this.post("/videos", requestBody);
  }

  async postSubmit(
    choiceSet: ChoiceSet,
    settings: Settings,
  ): Promise<PostSubmitResponse> {
    const requestBody: PostSubmitRequest = {
      choice_set: choiceSet,
      settings: settings,
    };
    return await this.post("/submit", requestBody);
  }

  async postUndo(recordId: string): Promise<PostUndoResponse> {
    const requestBody: PostUndoRequest = { record_id: recordId };
    return await this.post("/undo", requestBody);
  }

  async postSkip(
    choiceSet: ChoiceSet,
    settings: Settings,
  ): Promise<PostSkipResponse> {
    const requestBody: PostSkipRequest = {
      choice_set: choiceSet,
      settings: settings,
    };
    return await this.post("/skip", requestBody);
  }

  async postRankings(
    pageNumber: number,
    pageSize: number,
  ): Promise<PostRankingsResponse> {
    const requestBody: PostRankingsRequest = {
      page_number: pageNumber,
      page_size: pageSize,
    };
    return await this.post("/rankings", requestBody);
  }

  async get<ResT>(path: string): Promise<ResT> {
    const response = await fetch(`${this.apiBaseUrl}${path}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    await this.throwOnError(response);
    return await response.json();
  }

  async post<ReqT, ResT>(path: string, body: ReqT): Promise<ResT> {
    const response = await fetch(`${this.apiBaseUrl}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
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
