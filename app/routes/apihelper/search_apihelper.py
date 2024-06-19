from datetime import datetime
from typing import List, Optional


def normalize_string(s: Optional[str]) -> str:
    return s.replace(" ", "")

def search_id(id: int) -> dict:
    return {
        {"id":id}
    }

def search_titles(term: List[str], and_or: Optional[str]) -> dict:
    return {
        and_or: [
            {"title": {"$regex": ".*".join(normalize_string(title)), "$options": "i"}}
            for title in term
        ]
    }


def search_genres(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"genre": {"$regex": genre, "$options": "i"}} for genre in term]}


def search_overviews(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"overview": {"$regex": keyword, "$options": "i"}} for keyword in term]}


def search_directors(term: List[str], and_or: Optional[str]) -> dict:
    directors = [i.replace(" ", "") for i in term]
    regex_pattern = [f".*{''.join(f'(?=.*{char})' for char in i)}.*" for i in directors]
    return {
        and_or: [
            {"director": {"$elemMatch": {"$regex": regex, "$options": "i"}}}
            for regex in regex_pattern
        ]
    }


def search_actors(term: List[str], and_or: Optional[str]) -> dict:
    actors = [i.replace(" ", "") for i in term]
    regex_pattern = [f".*{''.join(f'(?=.*{char})' for char in i)}.*" for i in actors]
    return {
        and_or: [
            {"actor": {"$elemMatch": {"$regex": regex, "$options": "i"}}} for regex in regex_pattern
        ]
    }


def search_countries(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"origin_country": {"$regex": country, "$options": "i"}} for country in term]}


def search_platforms(term: List[str], and_or: Optional[str]) -> dict:
    return {and_or: [{"platform": {"$regex": platform, "$options": "i"}} for platform in term]}


def parse_date(date_str: Optional[str]) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def search_periods(start: Optional[str], end: Optional[str]) -> dict:
    # 날짜 범위 설정
    start_date_obj = parse_date(start) if start else datetime(1990, 1, 1)
    end_date_obj = parse_date(end) if end else datetime.today()

    return {"release_date": {"$gte": start_date_obj, "$lte": end_date_obj}}
