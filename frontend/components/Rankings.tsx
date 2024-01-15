"use client";

import { ClockCountdown, WarningOctagon } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Client } from "@/lib/client";
import { Ranking } from "@/lib/ranking";
import { cn } from "@/lib/styleUtilities";
import { Button } from "widgets/Button";
import { Video } from "./Video";

const PAGE_SIZE = 8;

export function Rankings() {
  const client = new Client();
  const [rankings, setRankings] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [currentPage, setCurrentPage] = useState<number>(0);

  const numPages = Math.ceil(rankings.length / PAGE_SIZE);

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

  function getPageRankings(pageNumber: number): Ranking[] {
    return rankings.slice(
      pageNumber * PAGE_SIZE,
      pageNumber * PAGE_SIZE + PAGE_SIZE,
    );
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
        <div className="flex h-full flex-col justify-center space-y-10">
          <div className="flex flex-wrap justify-center">
            {getPageRankings(currentPage).map((ranking, i) => (
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
                  <div className="absolute right-3 top-2 flex h-8 w-8 flex-col items-center justify-center rounded-full bg-stone-900/70 text-center text-sm text-stone-100">
                    {Math.floor(ranking.score)}
                  </div>
                </a>
              </div>
            ))}
          </div>
          <div className="flex w-full flex-row justify-center space-x-[2px]">
            {new Array(numPages)
              .fill(0)
              .map((_, x) => x + 1)
              .map((page) => (
                <Button
                  className={cn(
                    "px-3",
                    page === currentPage + 1 && "bg-stone-300 text-stone-800",
                  )}
                  key={page}
                  text={`${page}`}
                  onClick={() => setCurrentPage(page - 1)}
                />
              ))}
          </div>
        </div>
      )}
    </>
  );
}
