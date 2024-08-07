"use client";

import {
  CaretLeft,
  CaretRight,
  ClockCountdown,
  WarningOctagon,
} from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import { Video } from "@/components/video";
import { Client } from "@/lib/client";
import { Ranking } from "@/lib/models/ranking";
import { cn } from "@/lib/utilities/style-utilities";
import { Button } from "widgets/button";

const PAGE_SIZE = 8;

type PageVisibility = {
  visible: boolean;
  opacity: number;
};

export function Rankings() {
  const client = new Client();
  const [rankingsPage, setRankingsPage] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [currentPageNumber, setCurrentPageNumber] = useState<number>(1);
  const [numPages, setNumPages] = useState<number>(0);

  useEffect(() => {
    fetchRankings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPageNumber]);

  function fetchRankings() {
    setLoading(true);
    client
      .postRankings(currentPageNumber, PAGE_SIZE)
      .then((response) => {
        setRankingsPage(response.rankings_page);
        setNumPages(response.n_pages);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch videos: ", error);
        setLoading(false);
      });
  }

  function getPageVisibility(pageNumber: number): PageVisibility {
    const dist = Math.abs(pageNumber - currentPageNumber);
    const maxDist = 6.0;
    return {
      visible: dist < maxDist,
      opacity: (maxDist - dist) / maxDist,
    };
  }

  function canPageToOffset(offset: number) {
    const newPageNumber = currentPageNumber + offset;
    if (newPageNumber < 1 || newPageNumber >= numPages) {
      return false;
    }
    return true;
  }

  function offsetPage(offset: number) {
    if (!canPageToOffset(offset)) return;
    setCurrentPageNumber((currentPageNumber) => currentPageNumber + offset);
  }

  return (
    <>
      {loading && (
        <div className="flex h-full flex-col items-center justify-center gap-5 text-stone-600">
          <div className="text-4xl font-bold">Loading</div>
          <ClockCountdown size={80} color="#3e8fda" />
        </div>
      )}

      {!loading && rankingsPage.length === 0 && (
        <div className="flex h-full flex-col items-center justify-center gap-5 text-stone-600">
          <div className="text-4xl font-bold">Failed to fetch videos</div>
          <WarningOctagon size={80} color="#f08080" />
        </div>
      )}

      {!loading && rankingsPage.length > 0 && (
        <div className="flex h-full flex-col justify-center gap-10">
          <div className="flex flex-wrap justify-center">
            {rankingsPage.map((ranking) => (
              <Video
                key={ranking.video.id}
                video={ranking.video}
                onClick={() => {}}
                action="nothing"
                isCurrent={false}
                rating={ranking.rating}
              />
            ))}
          </div>
          <div className="flex w-full flex-col items-center justify-center gap-1">
            <div className="flex flex-row justify-center gap-[2px]">
              {new Array(numPages)
                .fill(0)
                .map((_, x) => x + 1)
                .map((pageNumber) => {
                  const pageVisibility = getPageVisibility(pageNumber);
                  return (
                    <Button
                      className={cn(
                        "px-3",
                        pageNumber === currentPageNumber &&
                          "bg-stone-300 text-stone-800",
                        !pageVisibility.visible && "hidden",
                        pageVisibility.opacity < 1.0 && "opacity-90",
                        pageVisibility.opacity < 0.8 && "opacity-70",
                        pageVisibility.opacity < 0.6 && "opacity-50",
                        pageVisibility.opacity < 0.4 && "opacity-30",
                      )}
                      key={pageNumber}
                      text={`${pageNumber}`}
                      onClick={() => setCurrentPageNumber(pageNumber)}
                    />
                  );
                })}
            </div>
            <div className="flex flex-row gap-1 pb-8">
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
