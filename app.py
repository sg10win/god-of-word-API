# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
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

# Load all clues from JSON file
with open("clues.json", "r", encoding="utf-8") as f:
    all_clues = json.load(f)

current_index = 0
today_views = 0
alltime_views = 0

@app.get("/api/clue-of-the-day")
def get_clue_of_the_day(current_index=current_index, today_views=today_views, alltime_views=alltime_views):
    today_index = datetime.utcnow().timetuple().tm_yday % len(all_clues)
    clue = all_clues[today_index]
    if current_index != today_index:
        current_index = today_index
        today_views = 0
    today_views += 1
    alltime_views += 1
    return {
        "hint1": " "+clue["hint1"],
        "hint2": " "+clue["hint2"],
        "hint3": " "+clue["hint3"],
        "answers": clue["answers"]
    }

# @app.get("/api/rating")
# def rating():
#     return {
#         "current index": current_index,
#         "today_views": today_views,
#         "alltime_views": alltime_views
#     }
