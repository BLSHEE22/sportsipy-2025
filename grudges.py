from sportsipy.nba.roster import Roster as NBARoster
from sportsipy.nba.roster import Player as NBAPlayer
from sportsipy.nfl.roster import Roster as NFLRoster
from sportsipy.nfl.roster import Player as NFLPlayer
from time import sleep
import sqlite3

# COLORS
BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

# GLOBALS
sports = ["NBA", "NFL"]
teams = {"NBA":["ATL", "BOS", "BRK", "CHI", "CHO", "CLE", "DAL", "DEN", "DET", "GSW", 
                "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", 
                "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"], 
         "NFL":["ATL", "BUF", "CAR", "CHI", "CIN", "CLE", "CLT", "CRD", "DAL", "DEN", 
                "DET", "GNB", "HTX", "JAX", "KAN", "MIA", "MIN", "NOR", "NWE", "NYG",
                "NYJ", "OTI", "PHI", "PIT", "RAI", "RAM", "RAV", "SDG", "SEA", "SFO", 
                "TAM", "WAS"]}
nfl_schedule = [[("DAL", "PHI"), ("KAN", "SDG"), ("TAM", "ATL"), ("CIN", "CLE"), ("MIA", "CLT"), # 1
                 ("CAR", "JAX"), ("RAI", "NWE"), ("CRD", "NOR"), ("PIT", "NYJ"), ("NYG", "WAS"),
                 ("OTI", "DEN"), ("SFO", "SEA"), ("DET", "GNB"), ("HTX", "RAM"), ("RAV", "BUF"),
                 ("MIN", "CHI")],
                [("WAS", "GNB"), ("CLE", "RAV"), ("JAX", "CIN"), ("NYG", "DAL"), ("CHI", "DET"), # 2
                 ("NWE", "MIA"), ("SFO", "NOR"), ("BUF", "NYJ"), ("SEA", "PIT"), ("RAM", "OTI"),
                 ("CAR", "CRD"), ("DEN", "CLT"), ("PHI", "KAN"), ("ATL", "MIN"), ("TAM", "HTX"),
                 ("SDG", "RAI")],
                [("MIA", "BUF"), ("ATL", "CAR"), ("GNB", "CLE"), ("HTX", "JAX"), ("CIN", "MIN"), # 3
                 ("PIT", "NWE"), ("RAM", "PHI"), ("NYJ", "TAM"), ("CLT", "OTI"), ("RAI", "WAS"), 
                 ("DEN", "SDG"), ("NOR", "SEA"), ("DAL", "CHI"), ("CRD", "SFO"), ("KAN", "NYG"),
                 ("DET", "RAV")],
                [("SEA", "CRD"), ("MIN", "PIT"), ("WAS", "ATL"), ("NOR", "BUF"), ("CLE", "DET"), # 4
                 ("OTI", "HTX"), ("CAR", "NWE"), ("SDG", "NYG"), ("PHI", "TAM"), ("CLT", "RAM"), 
                 ("JAX", "SFO"), ("RAV", "KAN"), ("CHI", "RAI"), ("GNB", "DAL"), ("NYJ", "MIA"), 
                 ("CIN", "DEN")],
                [("SFO", "RAM"), ("MIN", "CLE"), ("HTX", "RAV"), ("MIA", "CAR"), ("RAI", "CLT"), # 5
                 ("NYG", "NOR"), ("DAL", "NYJ"), ("DEN", "PHI"), ("OTI", "CRD"), ("TAM", "SEA"), 
                 ("DET", "CIN"), ("WAS", "SDG"), ("NWE", "BUF"), ("KAN", "JAX")],
                [("PHI", "NYG"), ("DEN", "NYJ"), ("RAM", "RAV"), ("DAL", "CAR"), ("CRD", "CLT"), # 6
                 ("SEA", "JAX"), ("SDG", "MIA"), ("CLE", "PIT"), ("SFO", "TAM"), ("OTI", "RAI"), 
                 ("CIN", "GNB"), ("NWE", "NOR"), ("DET", "KAN"), ("BUF", "ATL"), ("CHI", "WAS")],
                [("PIT", "CIN"), ("RAM", "JAX"), ("NOR", "CHI"), ("MIA", "CLE"), ("RAI", "KAN"), # 7 
                 ("PHI", "MIN"), ("CAR", "NYJ"), ("NWE", "OTI"), ("NYG", "DEN"), ("CLT", "SDG"), 
                 ("GNB", "CRD"), ("WAS", "DAL"), ("ATL", "SFO"), ("TAM", "DET"), ("HTX", "SEA")],
                [("MIN", "SDG"), ("MIA", "ATL"), ("CHI", "RAV"), ("BUF", "CAR"), ("NYJ", "CIN"), # 8 
                 ("SFO", "HTX"), ("CLE", "NWE"), ("NYG", "PHI"), ("TAM", "NOR"), ("DAL", "DEN"), 
                 ("OTI", "CLT"), ("GNB", "PIT"), ("WAS", "KAN")],
                [("RAV", "MIA"), ("CHI", "CIN"), ("MIN", "DET"), ("CAR", "GNB"), ("DEN", "HTX"), # 9
                 ("ATL", "NWE"), ("SFO", "NYG"), ("CLT", "PIT"), ("SDG", "OTI"), ("NOR", "RAM"), 
                 ("JAX", "RAI"), ("KAN", "BUF"), ("SEA", "WAS"), ("CRD", "DAL")],
                [("RAI", "DEN"), ("ATL", "CLT"), ("NOR", "CAR"), ("NYG", "CHI"), ("JAX", "HTX"), # 10
                 ("BUF", "MIA"), ("RAV", "MIN"), ("CLE", "NYJ"), ("NWE", "TAM"), ("CRD", "SEA"), 
                 ("RAM", "SFO"), ("DET", "WAS"), ("PIT", "SDG"), ("PHI", "GNB")],
                [("NYJ", "NWE"), ("WAS", "MIA"), ("CAR", "ATL"), ("TAM", "BUF"), ("SDG", "JAX"), # 11 
                 ("CHI", "MIN"), ("GNB", "NYG"), ("CIN", "PIT"), ("HTX", "OTI"), ("SFO", "CRD"), 
                 ("SEA", "RAM"), ("RAV", "CLE"), ("KAN", "DEN"), ("DET", "PHI"), ("DAL", "RAI")], # 12
                [("BUF", "HTX"), ("NYJ", "RAV"), ("PIT", "CHI"), ("NWE", "CIN"), ("NYG", "DET"), 
                 ("MIN", "GNB"), ("CLT", "KAN"), ("SEA", "OTI"), ("JAX", "CRD"), ("CLE", "RAI"), 
                 ("PHI", "DAL"), ("ATL", "NOR"), ("TAM", "RAM"), ("CAR", "SFO")],
                [("GNB", "DET"), ("KAN", "DAL"), ("CIN", "RAV"), ("CHI", "PHI"), ("RAM", "CAR"), # 13
                 ("SFO", "CLE"), ("HTX", "CLT"), ("NOR", "MIA"), ("ATL", "NYJ"), ("CRD", "TAM"), 
                 ("JAX", "OTI"), ("MIN", "SEA"), ("RAI", "SDG"), ("BUF", "PIT"), ("DEN", "WAS"),
                 ("NYG", "NWE")],
                [("DAL", "DET"), ("SEA", "ATL"), ("PIT", "RAV"), ("OTI", "CLE"), ("CHI", "GNB"), # 14
                 ("CLT", "JAX"), ("WAS", "MIN"), ("MIA", "NYJ"), ("NOR", "TAM"), ("DEN", "RAI"), 
                 ("RAM", "CRD"), ("CIN", "BUF"), ("HTX", "KAN"), ("PHI", "SDG")],
                [("ATL", "TAM"), ("CLE", "CHI"), ("RAV", "CIN"), ("CRD", "HTX"), ("NYJ", "JAX"), # 15
                 ("SDG", "KAN"), ("BUF", "NWE"), ("WAS", "NYG"), ("RAI", "PHI"), ("GNB", "DEN"), 
                 ("DET", "RAM"), ("CAR", "NOR"), ("CLT", "SEA"), ("OTI", "SFO"), ("MIN", "DAL"),
                 ("MIA", "PIT")],
                [("RAM", "SEA"), ("NWE", "RAV"), ("TAM", "CAR"), ("BUF", "CLE"), ("SDG", "DAL"), # 16
                 ("NYJ", "NOR"), ("MIN", "NYG"), ("KAN", "OTI"), ("ATL", "CRD"), ("JAX", "DEN"), 
                 ("PIT", "DET"), ("RAI", "HTX"), ("CIN", "MIA"), ("SFO", "CLT"), ("GNB", "CHI"),
                 ("PHI", "WAS")],
                [("DAL", "WAS"), ("DET", "MIN"), ("DEN", "KAN"), ("PIT", "CLE"), ("JAX", "CLT"), # 17
                 ("TAM", "MIA"), ("NWE", "NYJ"), ("NOR", "OTI"), ("PHI", "BUF"), ("CHI", "SFO"), 
                 ("RAM", "ATL"), ("SEA", "CAR"), ("CRD", "CIN"), ("RAV", "GNB"), ("HTX", "SDG"),
                 ("NYG", "RAI")],
                [("NOR", "ATL"), ("NYJ", "BUF"), ("DET", "CHI"), ("CLE", "CIN"), ("SDG", "DEN"), # 18
                 ("CLT", "HTX"), ("OTI", "JAX"), ("CRD", "RAM"), ("KAN", "RAI"), ("GNB", "MIN"), 
                 ("MIA", "NWE"), ("DAL", "NYG"), ("WAS", "PHI"), ("RAV", "PIT"), ("SEA", "SFO"), 
                 ("CAR", "TAM")]]
fantasy_positions = ["QB", "RB", "WR", "TE", "D/ST", "K"]
defensive_positions = ['DE', 'DT', 'DL', 'LB', 'DB', 'CB', "S"]
offensive_line_positions = ["T", "G", "C", "OL"]
utility_positions = ["FB", "LS", "P"]
position_translator = {"EDGE":"DE", "SAF":"S", "OT":"T", "FS":"S", "SS":"S", "OLB":"LB",
                       "ILB":"LB", "OG":"G", "Unknown":"Unknown", "NT":"DT", "RILB":"LB",
                       "MLB":"LB", "LT":"T", "LG":"G", "RG":"G", "RT":"T"}
playersWithGrudges = {}

def welcome():
    """
    Prints a instructional message upon running the script.
    """
    print("\n" + BOLD + "Welcome to Grudge Match Detector! " + RESET + "\n")
    print("When a player squares off against his/her previous team, " +
          "it is considered a \"grudge match.\"\n")
    print("Players with " + RED + "grudges" + RESET + " often perform better than " + 
          "what is usually expected of them.\n")
    print("Use this knowledge wisely!")

def ask(q, valid_options):
    """
    Prompts user for a specific sport/team/week.

    :param q: The question we are asking (e.g. sport/team/week).
    :type q: str
    :param valid_options: The acceptable answers to the question.
    :type valid_options: list
    :return: The user's answer.
    :rtype: str
    """
    deciding = True
    while deciding:
        ans = input("\n" + q.capitalize() + "?\n").upper()
        if ans in valid_options:
            deciding = False
        else:
            print(f"\n\'{ans}\' is not a valid {q}.")
    return ans

def update_roster(sport, team):
    """
    Updates roster based on latest information from sports-reference.com.

    :param team: The professional sports team abbreviation (e.g. ATL, BOS).
    :type team: str
    """
    print(f"Grabbing latest {team} roster...")
    if sport == "NBA":
        NBARoster(team)
    if sport == "NFL":
        NFLRoster(team)    

def update_all_rosters(sport):
    """
    Updates all rosters for a sports league.

    :param team: The professional sports league (e.g. NBA, NFL).
    :type team: str
    """
    for team in teams[sport]:
        update_roster(team)
        print("Sleeping for 1 minute...")
        sleep(60)

def find_grudges(t1, t2):
    """
    1. Queries database for players which currently play for team `t1` and 
    have previously played for team `t2`.
     
    2. Stores matches into global `playersWithGrudges` according to position.

    :param t1: Current team.
    :type t1: str
    :param t2: Former team.
    :type t2: str
    """
    #print(f"\nSeeking {t1} players who have previously played for {t2}...")
    conn = sqlite3.connect('sportsipy/' + sport.lower() + '/players.db')
    c = conn.cursor()
    c.execute(f"""
              SELECT name, position, team, team_history FROM players WHERE 
              sport == '{sport}' AND team == '{t1}' AND instr(team_history, '{t2}') > 0""")
    rows = c.fetchall()
    for row in rows:
        name, position, curr_team, team_history = row
        position = position.strip()
        if "-" in position:
            pos_list = position.split("-")
        else:
            pos_list = [position]
        for pos in pos_list:
            all_pos = fantasy_positions + defensive_positions + \
                offensive_line_positions + utility_positions
            if pos not in all_pos:
                pos = position_translator[pos]
            try:
                playersWithGrudges[pos].append((name, t1, t2))
            except:
                playersWithGrudges[pos] = []
                playersWithGrudges[pos].append((name, t1, t2))

def find_grudges_in_slate(week):
    """
    Finds grudges within an entire week's matchup slate.

    :param week: The regular season week (e.g. 1-17).
    :type week: str
    """
    print(f"\nFinding all grudge matches in the {sport} week {week} slate...\n")
    slate = nfl_schedule[week-1]
    for matchup in slate:
        away_team, home_team = matchup
        find_grudges(away_team, home_team)
        find_grudges(home_team, away_team)

def count_dst_grudges():
    """
    1. Count D/ST player grudges per team and sort by highest-to-lowest.

    2. Add sublist of the top three entries to `playersWithGrudges` under 'D/ST'.
    """
    dst_grudges = {"D/ST":[]}
    for pos in playersWithGrudges.keys():
        if pos in defensive_positions:
            for player in playersWithGrudges[pos]:
                dst_grudges["D/ST"].append(player)
    dsts = [(g[1], g[2]) for g in dst_grudges["D/ST"]]
    dsts_temp = [(team[0], dsts.count(team), team[1]) for team in set(dsts)]
    dsts_sorted = sorted(dsts_temp, key=lambda x: x[1], reverse=True)[:3]
    dst_grudges["D/ST"] = dsts_sorted
    playersWithGrudges.update(dst_grudges)

def display_grudges(position_type, positions):
    """
    Print out player grudges by position.

    :param position_type: The print header for the output.
    :type position_type: str
    :param positions: The list of positions to print contents for.
    :type positions: list
    """
    print(GREEN + position_type + RESET + "\n")
    for pos in positions:
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

# START
welcome()
sport = ask("sport", sports)
week = ask("week", [str(i) for i in range(1, 19)])
find_grudges_in_slate(int(week))
dst_grudges = count_dst_grudges()
print("\n" + BOLD + "Players with Grudges:" + RESET + "\n")
display_grudges("FANTASY", fantasy_positions)
display_grudges("DEFENSE", defensive_positions)
display_grudges("OFFENSIVE LINE", offensive_line_positions)
display_grudges("UTILITY", utility_positions)
print()

#### NBA DEBUG
## TODO
## address 'detriot' typo (we need to re-update all rosters)
## - a player grudge against his/her original team is caled a 'primary grudge' 
##   (distinguish somehow!)
##   - for this we need to collect the player's drafted team and store in new column in DB
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

# team1 = ask("team 1", teams[sport])
# team2 = ask("team 2", teams[sport]) 
# sleep(5)
# find_grudges(sport, team1, team2)
# find_grudges(sport, team2, team1)

#### NFL DEBUG
## TODO
## - sort each position grouping by career games played
## - scrape for player's fantasy pos rk and display as part of output (could sort by pos rk as well)
## - extra indicator for if a player has ONLY previously played for the ex-team in question 
##   (bigger grudge!)
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
