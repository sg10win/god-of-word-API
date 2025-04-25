from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json

app = FastAPI()

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ratings = {
    "current_index": 0,
    "today_views": 0,
    "alltime_views": 0
}

# Load and sort clues by their `index` field
with open("clues.json", "r", encoding="utf-8") as f:
    raw_clues = json.load(f)
    all_clues = sorted(raw_clues, key=lambda clue: clue["index"])

def get_sorted_index_at_21utc():
    now = datetime.utcnow()
    # If current time is before 21:00 UTC, use yesterday's index
    if now.hour < 21:
        clue_day = now - timedelta(days=1)
    else:
        clue_day = now
    # Determine which clue to show based on days passed
    index = clue_day.timetuple().tm_yday % len(all_clues)
    return index

@app.get("/api/clue-of-the-day")
def get_clue_of_the_day():
    clue_index = get_sorted_index_at_21utc()
    clue = all_clues[clue_index]
    global ratings
    if ratings["current_index"] != clue_index:
        ratings["current_index"] = clue_index
        ratings["today_views"] = 0
    ratings["today_views"] += 1
    ratings["alltime_views"] += 1

    return {
        "hint1": " " + clue["hint1"],
        "hint2": " " + clue["hint2"],
        "hint3": " " + clue["hint3"],
        "answers": clue["answers"]
    }

@app.get("/api/rating")
def rating():
    return ratings
