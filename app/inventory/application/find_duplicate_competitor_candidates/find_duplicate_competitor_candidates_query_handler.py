from collections import defaultdict
from itertools import combinations

from rapidfuzz import fuzz

from inventory.domain.competitor import Competitor
from inventory.domain.repositories.competitor_criteria import CompetitorCriteria
from inventory.domain.repositories.competitor_repository import CompetitorRepository

from inventory.application.find_duplicate_competitor_candidates.duplicate_candidate_group import (
    DuplicateCandidateGroup,
)
from inventory.application.find_duplicate_competitor_candidates.find_duplicate_competitor_candidates_query import (
    FindDuplicateCompetitorCandidatesQuery,
)


class FindDuplicateCompetitorCandidatesQueryHandler:
    def __init__(self, competitor_repository: CompetitorRepository):
        self.competitor_repository = competitor_repository

    def handle(self, query: FindDuplicateCompetitorCandidatesQuery) -> list[DuplicateCandidateGroup]:
        competitors = self.competitor_repository.find_by_criteria(CompetitorCriteria())

        by_normalized_name: dict[str, list[Competitor]] = defaultdict(list)
        for competitor in competitors:
            by_normalized_name[competitor.name_normalized].append(competitor)

        exact_groups = [
            DuplicateCandidateGroup(competitors=group, score=1.0, match_reason="exact_normalized")
            for group in by_normalized_name.values()
            if len(group) > 1
        ]

        ungrouped = [group[0] for group in by_normalized_name.values() if len(group) == 1]
        fuzzy_groups = []
        for a, b in combinations(ungrouped, 2):
            score = fuzz.token_sort_ratio(a.name_normalized, b.name_normalized) / 100.0
            if score >= query.similarity_threshold:
                fuzzy_groups.append(DuplicateCandidateGroup(competitors=[a, b], score=score, match_reason="fuzzy"))

        fuzzy_groups.sort(key=lambda group: group.score, reverse=True)

        return exact_groups + fuzzy_groups
