import { MatchingStrategy } from "@/lib/models/matchingStrategy";

export type MatchingSettings = {
  matching_strategy: MatchingStrategy;
  balanced_random_fraction: number;
};
