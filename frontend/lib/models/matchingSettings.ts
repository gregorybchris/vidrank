import { Nullable } from "../utilities/typeUtilities";

export type ByDateStrategySettings = {
  days: number;
};

export type ByRatingStrategySettings = {};

export type FinetuneStrategySettings = {
  fraction: number;
};

export type RandomStrategySettings = {};

export type MatchingSettings = {
  by_date_strategy: Nullable<ByDateStrategySettings>;
  by_rating_strategy: Nullable<ByRatingStrategySettings>;
  finetune_strategy: Nullable<FinetuneStrategySettings>;
  random_strategy: Nullable<RandomStrategySettings>;
};
