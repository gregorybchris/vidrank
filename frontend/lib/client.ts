import { Video } from "./video";

export type GetVideosResponseBody = {
  videos: Video[];
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
}
