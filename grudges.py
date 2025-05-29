from sportsipy.nba.roster import Roster as NBARoster
from sportsipy.nba.roster import Player as NBAPlayer
from sportsipy.nfl.roster import Roster as NFLRoster
from sportsipy.nfl.roster import Player as NFLPlayer
from time import sleep
import ast
import sqlite3

# COLORS
BOLD = '\033[1m'
RESET = '\033[0m'

sports = ["NBA", "NFL"]
teams = {"NBA":["ATL", "BOS", "BRK", "CHI", "CHO", "CLE", "DAL", "DEN", "DET", "GSW", 
                "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", 
                "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"], 
         "NFL":["ATL", "BUF", "CAR", "CHI", "CIN", "CLE", "CLT", "CRD", "DAL", "DEN", 
                "DET", "GNB", "HTX", "JAX", "KAN", "MIA", "MIN", "NOR", "NWE", "NYG",
                "NYJ", "OTI", "PHI", "PIT", "RAI", "RAM", "RAV", "SDG", "SEA", "SFO", 
                "TAM", "WAS"]}
playersWithGrudges = []

def welcome():
    print("\n" + BOLD + "Welcome to Grudge Match Detector! " + RESET + "\n")
    print("When a player squares off against his/her previous team, it is considered a \"grudge match.\"\n")
    print("Players with grudges often perform better than expected.\n")
    print("Use this knowledge wisely!\n")

def decide(s, valid_options):
    deciding = True
    while deciding:
        ans = input(s.capitalize() + "?\n").upper()
        if ans in valid_options:
            deciding = False
        else:
            print(f"\'{ans}\' is not a valid {s}.")
    return ans

def get_latest_roster(sport, team):
    print(f"Grabbing latest {team} roster...")
    if sport == "NBA":
        NBARoster(team)
    if sport == "NFL":
        NFLRoster(team)     

def find_grudges_db(sport, t1, t2):
    print(f"Seeking {t1} players who have previously played for {t2}...")
    conn = sqlite3.connect('sportsipy/' + sport.lower() + '/players.db')
    c = conn.cursor()
    c.execute(f"SELECT name, team, team_history FROM players WHERE sport == '{sport}' AND team == '{t1}'")
    rows = c.fetchall()
    for row in rows:
        name, team, team_history = row
        team_history = ast.literal_eval(team_history)
        if t2 in team_history:
            playersWithGrudges.append((name, t1, t2))

# START
welcome()
sport = decide("sport", sports)
team1 = decide("team 1", teams[sport])
team2 = decide("team 2", teams[sport]) 
sleep(5)
find_grudges_db(sport, team1, team2)
find_grudges_db(sport, team2, team1)
print("\n" + BOLD + "Players with Grudges:" + RESET + "\n")
for player, curr_team, former_team in playersWithGrudges:
    print(f"{player} ({curr_team}) has a grudge against {former_team}.")
print()

#### NBA DEBUG
## TODO
## - sort player grudges by highest to lowest career avg minutes per game
# player1 = NBAPlayer('armstta02')
# print(f"Name: {player1.name}")
# print(f"Season(s): {player1.season}")
# print(f"Height: {player1.height}")
# print(f"Weight: {player1.weight}")
# print(f"Position: {player1.position}")
# print(f"Birth Date: {player1.birth_date}")
# print(f"Nationality: {player1.nationality}")
# print(f"Team History: {player1.team_history}")
# print(f"Current Team: {player1.team_abbreviation}")
# print(f"Games Played: {player1.games_played}")
# print(f"Games Started: {player1.games_started}")

#### NFL DEBUG
## TODO
## - be able to handle an entire slate of matchups
# player1 = NFLPlayer('DaniJa02')
# print(f"Name: {player1.name}")
# print(f"Experience: {player1.season}")
# print(f"Height: {player1.height}")
# print(f"Weight: {player1.weight}")
# print(f"Position: {player1.position}")
# print(f"Birth Date: {player1.birth_date}")
# print(f"Team History: {player1.team_history}")
# print(f"Current Team: {player1.team_abbreviation}")

## CCBL? TODO
# Figure out how to write to database
# Figure out how to host on github.io website
# Figure out front end!
