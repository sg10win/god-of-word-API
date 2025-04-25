from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
import random
import hashlib

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
    "current_index": -1,
    "today_views": 0,
    "alltime_views": 0
}

# Load clues from JSON file
with open("clues.json", "r", encoding="utf-8") as f:
    all_clues = json.load(f)

def get_daily_random_index():
    now = datetime.utcnow()
    if now.hour < 21:
        clue_day = now - timedelta(days=1)
    else:
        clue_day = now

    # Generate a deterministic "random" seed from the date
    seed_str = clue_day.strftime("%Y-%m-%d")
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    random.seed(seed)
    return random.randint(0, len(all_clues) - 1)

@app.get("/api/clue-of-the-day")
def get_clue_of_the_day():
    clue_index = get_daily_random_index()
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
