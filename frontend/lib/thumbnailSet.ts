import { Thumbnail } from "@/lib/thumbnail";
import { Optional } from "./typeUtilities";

export type ThumbnailSet = {
  default: Optional<Thumbnail>;
  standard: Optional<Thumbnail>;
  medium: Optional<Thumbnail>;
  high: Optional<Thumbnail>;
  maxres: Optional<Thumbnail>;
};

export function getLargestThumbnail(thumbnailSet: ThumbnailSet): Optional<Thumbnail> {
  const thumbnails = [
    thumbnailSet.maxres,
    thumbnailSet.high,
    thumbnailSet.medium,
    thumbnailSet.standard,
    thumbnailSet.default,
  ];

  for (const thumbnail of thumbnails) {
    if (thumbnail) {
      return thumbnail;
    }
  }

  return undefined;
}
