import os
import sys
import argparse
import requests
import functools
import pickle
import hashlib
from typing import List, Dict
from pathlib import Path


def persistent_cache():
    cache_file = Path(__file__).parent / "cache.pkl"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                cache = pickle.load(f)
        except Exception:
            cache = {}
    else:
        cache = {}

    keys = list(cache.keys())
    if len(keys) > 6:
        cache.pop(keys[0])

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key_data = (func.__name__, args, tuple(sorted(kwargs.items())))
            key = hashlib.sha256(pickle.dumps(key_data)).hexdigest()

            if key in cache:
                return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result

            with open(cache_file, "wb") as f:
                pickle.dump(cache, f)

            return result

        return wrapper
    return decorator

@persistent_cache()
def _get_activity(user: str) -> List[Dict]:
    response = requests.get(f"https://api.github.com/users/{user}/events").json()
    if isinstance(response, dict):
        print(f"API error or the user {user} does not exist.")
        sys.exit()

    return response

def activity(user: str) -> None:
    activity_data = {}
    data = _get_activity(user)

    for event in data:
        event_type = event.get("type")
        event_repo = event.get("repo")
        event_repo_id = event_repo.get("id")
        event_repo_name = event_repo.get("name")

        if event_type not in activity_data:
            activity_data[event_type] = {}

        if event_repo_id not in activity_data[event_type]:
            activity_data[event_type][event_repo_id] = {"name": event_repo_name, "count": 1}
        else:
            activity_data[event_type][event_repo_id]["count"] += 1

    for event, repos in activity_data.items():
        for _, details in repos.items():
            print(f"{event} {details.get('count')} times in {details.get('name')}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Github activity tool.")
    subparser = parser.add_subparsers(dest="command", required=True)

    github_parser = subparser.add_parser("activity", help="Get the activity from github API.")
    github_parser.add_argument("--user", "-u", type=str, required=True, help="User to get the activity from.")

    args = parser.parse_args()

    if args.command == "activity":
        activity(args.user)

if __name__ == "__main__":
    main()