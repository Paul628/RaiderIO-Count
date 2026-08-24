# Using the Raider.IO API to get the overall runs of all seasons for a given character.

import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

possible_seasons = [
    "season-7.2.0",
    "season-7.2.5",
    "season-7.3.0",
    "season-7.3.2",
    "season-post-legion",
    "season-pre-bfa",
    "season-bfa-1",
    "season-bfa-2",
    "season-bfa-2-post",
    "season-bfa-3",
    "season-bfa-3-post",
    "season-bfa-4",
    "season-bfa-4-post",
    #"season-sl-1",
    "season-sl-1-post",
    "season-sl-2",
    "season-sl-2-legion-timewalking",
    #"season-sl-2-post-915",
    #"season-sl-2-post",
    "season-sl-3",
    "season-sl-3-legion-timewalking",
    #"season-sl-3-post-925",
    "season-sl-4",
    "season-sl-4-break-the-meta",
    "season-sl-4-legion-timewalking",
    #"season-sl-4-patch-10-0",
    "season-sl-4-post",
    "season-df-1",
    "season-df-1-post",
    "season-df-1-break-the-meta",
    "season-df-2",
    #"season-df-2-post",
    #"season-df-2-post-1015",
    #"season-df-2-post-1017",
    "season-df-2-break-the-meta",
    "season-df-3",
    "season-df-3-meta-vs-meta",
    "season-df-3-break-the-meta",
    #"season-df-4",
    "season-df-4-cutoffs",
    "season-df-4-post",
    "season-df-4-break-the-meta",
    "season-tww-1",
    "season-tww-1-post",
    "season-tww-1-break-the-meta",
    "season-tww-2",
    "season-tww-2-break-the-meta",
    "season-tww-2-meta-vs-meta",
    #"season-tww-3",
    "season-tww-3-cutoffs",
    "season-tww-3-break-the-meta",
    "season-tww-3-legion-remix",
    "season-tww-3-legion-remix-1-player",
    "season-mn-1",
    "season-mn-1-break-the-meta",
    "season-mn-2"
]

def get_raiderio_runs(access_key,region, realm, character_name,fields):
    # API
    url = f"https://raider.io/api/v1/characters/profile?access_key={access_key}&region={region}&realm={realm}&name={character_name}&fields={fields}"
    response = requests.get(url)
    # See if we could find the character
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: Unable to fetch data for {character_name} on {realm} ({region}). Status code: {response.status_code}")
        return None

access_key = os.environ.get("API_KEY")
#print(access_key)
region = input("Enter the region (e.g. us, eu): ")
realm = input("Enter the realm (e.g. blackhand): ")
character_name = input("Enter the character name: ")

total_runs = 0
raiderio_data = {}
csv_rows = []

for season in possible_seasons:
    fields = f"mythic_plus_dungeon_run_counts:{season}"
    raiderio_data = get_raiderio_runs(access_key, region, realm, character_name,fields)
    # Iterate through the data and sum up all the 'season_runs_total' values.
    if raiderio_data:
        season_dungeons = raiderio_data["mythic_plus_dungeon_run_counts"]
        runs_in_season = sum(dungeon["season_runs_total"] for dungeon in season_dungeons)
        total_runs += runs_in_season

        for dungeon in season_dungeons:
            csv_rows.append({
                "season": season,
                "dungeon": dungeon.get("dungeon") or dungeon.get("name") or dungeon.get("short_name") or "Unknown",
                "runs_in_season": dungeon["season_runs_total"],
                "total_runs": total_runs,
            })

        print(f"Season {season} -> Runs in season: {runs_in_season} / Total runs: {total_runs}")

csv_filename = f"{character_name}-{realm}_raiderio_runs.csv"
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=["season", "dungeon", "runs_in_season", "total_runs"],
    )
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"CSV written to {csv_filename}")
