import requests
import csv

apiKey = "" #api key
idURL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?regions=us&oddsFormat=american&apiKey=" + apiKey

idResponse = requests.get(idURL)
data = idResponse.json()

try:
    gameIDs = [i["id"] for i in data]
except TypeError:
    print("invalid API key")
    exit(1)

props = ["player_pass_yds", "player_reception_yds", "player_rush_yds"]

with open('suggestedPicks.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Player', 'o/u', 'Line', 'Stat', 'Odds'])

    for ids in gameIDs:
        for stat in props:
            gameURL = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{ids}/odds?apiKey={apiKey}&regions=us&markets={stat}&oddsFormat=american"
            gameResponse = requests.get(gameURL)
            gameData = gameResponse.json()

            outcomes = [outcome for bookmaker in gameData.get("bookmakers", []) for outcome in bookmaker.get("markets", [])[0].get("outcomes", [])]

            for outcome in outcomes:
                if int(outcome.get("price", 0)) <= -130 and int(outcome.get("price", 0)) >= -200:
                    csvwriter.writerow([
                        outcome.get('description', ''),
                        outcome.get('name', ''),
                        outcome.get('point', ''),
                        stat,
                        outcome.get('price', '')
                    ])
                    
