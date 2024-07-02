export type ByRatingStrategySettings = {};

export type FinetuneStrategySettings = {
  fraction: number;
};

export type RandomStrategySettings = {};

export type MatchingSettings = {
  by_rating_strategy: ByRatingStrategySettings | null;
  finetune_strategy: FinetuneStrategySettings | null;
  random_strategy: RandomStrategySettings | null;
};
