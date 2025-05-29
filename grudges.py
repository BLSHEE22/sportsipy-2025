from sportsipy.nba.roster import Roster as NBARoster
from sportsipy.nba.roster import Player as NBAPlayer
from sportsipy.nfl.roster import Roster as NFLRoster
from sportsipy.nfl.roster import Player as NFLPlayer
from time import sleep
import ast
import sqlite3

# COLORS
BOLD = '\033[1m'
RED = '\033[31m'
RESET = '\033[0m'

sports = ["NBA", "NFL"]
teams = {"NBA":["ATL", "BOS", "BRK", "CHI", "CHO", "CLE", "DAL", "DEN", "DET", "GSW", 
                "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", 
                "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"], 
         "NFL":["ATL", "BUF", "CAR", "CHI", "CIN", "CLE", "CLT", "CRD", "DAL", "DEN", 
                "DET", "GNB", "HTX", "JAX", "KAN", "MIA", "MIN", "NOR", "NWE", "NYG",
                "NYJ", "OTI", "PHI", "PIT", "RAI", "RAM", "RAV", "SDG", "SEA", "SFO", 
                "TAM", "WAS"]}
nfl_schedule = [[("DAL", "PHI"), ("KAN", "SDG"), ("TAM", "ATL"), ("CIN", "CLE"), ("MIA", "CLT"),
                 ("CAR", "JAX"), ("RAI", "NWE"), ("CRD", "NOR"), ("PIT", "NYJ"), ("NYG", "WAS"),
                 ("OTI", "DEN"), ("SFO", "SEA"), ("DET", "GNB"), ("HTX", "RAM"), ("RAV", "BUF"),
                 ("MIN", "CHI")],
                [(), ()],
                [(), ()],
                [(), ()],[],[],[],[],[],[],[],[],[],[],[],[],[]]
fantasy_positions = ["QB", "RB", "WR", "TE", "K", "DT", "DE", "DB", "CB"]
playersWithGrudges = {}

def welcome():
    print("\n" + BOLD + "Welcome to Grudge Match Detector! " + RESET + "\n")
    print("When a player squares off against his/her previous team, it is considered a \"grudge match.\"\n")
    print("Players with grudges often perform better than expected.\n")
    print("Use this knowledge wisely!")

def decide(s, valid_options):
    deciding = True
    while deciding:
        ans = input("\n" + s.capitalize() + "?\n").upper()
        if ans in valid_options:
            deciding = False
        else:
            print(f"\n\'{ans}\' is not a valid {s}.")
    return ans

def get_latest_roster(sport, team):
    print(f"Grabbing latest {team} roster...")
    if sport == "NBA":
        NBARoster(team)
    if sport == "NFL":
        NFLRoster(team)     

def find_grudges(sport, t1, t2):
    print(f"\nSeeking {t1} players who have previously played for {t2}...")
    conn = sqlite3.connect('sportsipy/' + sport.lower() + '/players.db')
    c = conn.cursor()
    c.execute(f"SELECT name, position, team, team_history FROM players WHERE sport == '{sport}' AND team == '{t1}'")
    rows = c.fetchall()
    for row in rows:
        name, position, curr_team, team_history = row
        team_history = ast.literal_eval(team_history)
        if t2 in team_history:
            try:
                playersWithGrudges[position].append((name, t1, t2))
            except:
                playersWithGrudges[position] = []
                playersWithGrudges[position].append((name, t1, t2))
            #playersWithGrudges.append(((name, position), t1, t2))

def find_grudges_in_slate(sport, week):
    print(f"\nFinding all grudge matches in the {sport} week {week} slate...\n")
    slate = nfl_schedule[week-1]
    for matchup in slate:
        away_team, home_team = matchup
        find_grudges(sport, away_team, home_team)
        find_grudges(sport, home_team, away_team)

# START
welcome()
#get_latest_roster('NFL', 'WAS')
sport = decide("sport", sports)
week = decide("week", [str(i) for i in range(1, 18)])
find_grudges_in_slate(sport, int(week))
print("\n" + BOLD + "Players with Grudges:" + RESET + "\n")
for pos in fantasy_positions:
    print(RED + f"{pos}" + RESET + "\n")
    try:
        players_at_position = playersWithGrudges[pos]
    except:
        print("None\n")
        continue
    for player_info in players_at_position:
        name, curr_team, former_team = player_info
        print(f"{name} ({curr_team}) has a grudge against {former_team}.")
    print()
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

# team1 = decide("team 1", teams[sport])
# team2 = decide("team 2", teams[sport]) 
# sleep(5)
# find_grudges(sport, team1, team2)
# find_grudges(sport, team2, team1)

#### NFL DEBUG
## TODO
## - be able to handle an entire slate of matchups
## - sort output by position
## - sort each position grouping by games played
# player1 = NFLPlayer('JoseGr00')
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
