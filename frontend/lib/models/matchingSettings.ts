export type ByDateStrategySettings = {
  days: number;
};

export type ByRatingStrategySettings = {};

export type FinetuneStrategySettings = {
  fraction: number;
};

export type RandomStrategySettings = {};

export type MatchingSettings = {
  by_date_strategy: ByDateStrategySettings | null;
  by_rating_strategy: ByRatingStrategySettings | null;
  finetune_strategy: FinetuneStrategySettings | null;
  random_strategy: RandomStrategySettings | null;
};
