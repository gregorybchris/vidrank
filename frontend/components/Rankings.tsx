"use client";

import { ClockCountdown, WarningOctagon } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { Ranking } from "@/lib/ranking";
import { Video } from "./Video";

export function Rankings() {
  const client = new Client();
  const [rankings, setRankings] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchRankings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function fetchRankings() {
    setLoading(true);
    client
      .getRankings()
      .then((response) => {
        console.log("Fetched rankings: ", response.rankings);
        setRankings(response.rankings);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch videos: ", error);
        setLoading(false);
      });
  }

  return (
    <>
      {loading && (
        <div className="flex h-full flex-col items-center justify-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Loading</div>
          <ClockCountdown size={80} color="#3e8fda" />
        </div>
      )}

      {!loading && rankings.length === 0 && (
        <div className="flex h-full flex-col items-center justify-center space-y-5 text-stone-600">
          <div className="text-4xl font-bold">Failed to fetch videos</div>
          <WarningOctagon size={80} color="#f08080" />
        </div>
      )}

      {!loading && rankings.length > 0 && (
        <div className="flex flex-wrap justify-center py-10">
          {rankings.map((ranking, i) => (
            <div key={i} className="relative">
              <a
                href={`https://www.youtube.com/watch?v=${ranking.video.id}`}
                target="_blank"
              >
                <Video
                  video={ranking.video}
                  onClick={() => {}}
                  action="nothing"
                  isCurrent={false}
                />
                <div className="absolute right-0 top-0 h-10 w-10 rounded-full bg-stone-900 pt-2 text-center text-stone-100">
                  {Math.floor(ranking.score)}
                </div>
              </a>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
