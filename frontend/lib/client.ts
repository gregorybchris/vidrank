import { ChoiceSet } from "@/lib/models/choiceSet";
import { MatchingStrategy } from "@/lib/models/matchingStrategy";
import { Ranking } from "@/lib/models/ranking";
import { Video } from "@/lib/models/video";

export type GetVideosResponseBody = {
  videos: Video[];
};

export type PostSubmitRequestBody = {
  choice_set: ChoiceSet;
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
  choice_set: ChoiceSet;
};

export type PostSkipResponseBody = {
  record_id: string;
  videos: Video[];
};

export type GetRankingsResponseBody = {
  rankings: Ranking[];
};

export class Client {
  async getVideos(
    matchingStrategy: MatchingStrategy,
  ): Promise<GetVideosResponseBody> {
    const params = new URLSearchParams({ matching_strategy: matchingStrategy });

    const response = await fetch("http://localhost:8000/videos?" + params, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postSubmit(choiceSet: ChoiceSet): Promise<PostSubmitResponseBody> {
    const requestBody: PostSubmitRequestBody = { choice_set: choiceSet };
    const response = await fetch("http://localhost:8000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postUndo(recordId: string): Promise<PostSkipResponseBody> {
    const requestBody: PostUndoRequestBody = { record_id: recordId };
    const response = await fetch("http://localhost:8000/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    await this.throwOnError(response);
    return await response.json();
  }

  async postSkip(choiceSet: ChoiceSet): Promise<PostSkipResponseBody> {
    const requestBody: PostSkipRequestBody = { choice_set: choiceSet };
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
