"use client";

import {
  CaretLeft,
  CaretRight,
  ClockCountdown,
  WarningOctagon,
} from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Video } from "@/components/Video";
import { Client } from "@/lib/client";
import { Ranking } from "@/lib/models/ranking";
import { cn } from "@/lib/utilities/styleUtilities";
import { Button } from "widgets/Button";

const PAGE_SIZE = 8;

type PageVisibility = {
  visible: boolean;
  opacity: number;
};

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

  function getPageRankings(page: number): Ranking[] {
    return rankings.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);
  }

  function getPageVisibility(page: number): PageVisibility {
    const dist = Math.abs(page - currentPage);
    const maxDist = 6.0;
    return {
      visible: dist < maxDist,
      opacity: (maxDist - dist) / maxDist,
    };
  }

  function canPageToOffset(offset: number) {
    const newPage = currentPage + offset;
    if (newPage < 0 || newPage >= numPages) {
      return false;
    }
    return true;
  }

  function offsetPage(offset: number) {
    if (!canPageToOffset(offset)) return;
    setCurrentPage((currentPage) => currentPage + offset);
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
                <Video
                  video={ranking.video}
                  onClick={() => {}}
                  action="nothing"
                  isCurrent={false}
                />
                <div className="absolute right-3 top-2 flex h-8 w-8 flex-col items-center justify-center rounded-full bg-stone-900/70 text-center text-sm text-stone-100">
                  {Math.round(ranking.rating)}
                </div>
              </div>
            ))}
          </div>
          <div className="flex w-full flex-col items-center justify-center space-y-1">
            <div className="flex flex-row justify-center space-x-[2px]">
              {new Array(numPages)
                .fill(0)
                .map((_, x) => x)
                .map((page) => {
                  const pageVisibility = getPageVisibility(page);
                  return (
                    <Button
                      className={cn(
                        "px-3",
                        page === currentPage && "bg-stone-300 text-stone-800",
                        !pageVisibility.visible && "hidden",
                        pageVisibility.opacity < 1.0 && "opacity-90",
                        pageVisibility.opacity < 0.8 && "opacity-70",
                        pageVisibility.opacity < 0.6 && "opacity-50",
                        pageVisibility.opacity < 0.4 && "opacity-30",
                      )}
                      key={page}
                      text={`${page + 1}`}
                      onClick={() => setCurrentPage(page)}
                    />
                  );
                })}
            </div>
            <div className="flex flex-row space-x-1">
              <div
                className={cn(
                  "p-1",
                  canPageToOffset(-1)
                    ? "cursor-pointer rounded transition-all hover:bg-stone-300"
                    : "opacity-40",
                )}
                onClick={() => offsetPage(-1)}
              >
                <CaretLeft size={24} color="#3e8fda" weight="duotone" />
              </div>
              <div
                className={cn(
                  "p-1",
                  canPageToOffset(1)
                    ? "cursor-pointer rounded transition-all hover:bg-stone-300"
                    : "opacity-40",
                )}
                onClick={() => offsetPage(1)}
              >
                <CaretRight size={24} color="#3e8fda" weight="duotone" />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
