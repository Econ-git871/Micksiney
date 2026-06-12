"""Score and rank jobs against a resume profile.

Scoring is intentionally transparent (no black-box embeddings):

    score(job) = Σ over matched profile-terms of  weight * idf(term)
                 + location bonus

where matched terms appearing in the job *title* get an extra weight, and
``idf`` down-weights terms that appear in almost every job. The raw score is
normalized to a 0–100 "fit" relative to the best job in the batch, so it reads
as "how well this job fits me compared to the others I'm looking at".
"""
from __future__ import annotations

import math

from . import lexicon
from .models import Job, ResumeProfile

TITLE_BONUS = 2.0      # extra weight when a term appears in the job title
LOCATION_BONUS = 1.5   # added when a profile city matches the job location


def _profile_terms(profile: ResumeProfile) -> list[str]:
    terms: list[str] = []
    for t in profile.keywords or (profile.skills + profile.titles):
        if t not in terms:
            terms.append(t)
    return terms


def score_jobs(profile: ResumeProfile, jobs: list[Job]) -> list[Job]:
    """Return ``jobs`` scored and sorted by descending fit (mutates ``score``)."""
    terms = _profile_terms(profile)
    if not jobs:
        return []

    job_texts = [
        f"{j.title}\n{j.title}\n{j.company}\n{j.description}".lower()
        for j in jobs
    ]  # title duplicated so title hits also count toward presence

    n = len(jobs)
    # concept_match expands each term to its cross-language synonyms (中↔英)
    df = {t: sum(1 for jt in job_texts if lexicon.concept_match(t, jt)) for t in terms}

    for job, jt in zip(jobs, job_texts):
        title_low = job.title.lower()
        loc_low = (job.location or "").lower()
        matched: list[str] = []
        raw = 0.0
        for term in terms:
            if not lexicon.concept_match(term, jt):
                continue
            idf = math.log(1 + n / (1 + df[term]))
            weight = 1.0 + (TITLE_BONUS if lexicon.concept_match(term, title_low) else 0.0)
            raw += weight * idf
            matched.append(term)
        if profile.cities and any(
            lexicon.term_in(c, loc_low) or lexicon.term_in(c, jt) for c in profile.cities
        ):
            raw += LOCATION_BONUS
        job.score = raw
        job.matched = matched

    best = max((j.score for j in jobs), default=0.0) or 1.0
    for job in jobs:
        job.score = round(100.0 * job.score / best, 1)

    return sorted(jobs, key=lambda j: j.score, reverse=True)


def top_matches(
    profile: ResumeProfile,
    jobs: list[Job],
    limit: int | None = None,
    min_score: float = 0.0,
) -> list[Job]:
    ranked = [j for j in score_jobs(profile, jobs) if j.score >= min_score]
    return ranked[:limit] if limit else ranked
