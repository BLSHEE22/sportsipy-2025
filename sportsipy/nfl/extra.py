# def find_grudges_in_slate(week):
#     """
#     Finds grudges within an entire week's matchup slate.

#     :param week: The regular season week (e.g. 1-17).
#     :type week: str
#     """
#     print(f"\nFinding all grudge matches in the {sport} week {week} slate...\n")
#     weekSlate = nfl_schedule[week-1]
#     for day, gameList in weekSlate:
#         for game in gameList:
#             time, away_team, home_team = game
#             find_grudges(day, time, away_team, home_team)
#             find_grudges(day, time, home_team, away_team)

# def count_dst_grudges():
#     """
#     1. Count D/ST player grudges per team and sort by highest-to-lowest.

#     2. Add sublist of the top three entries to `playersWithGrudges` under 'D/ST'.
#     """
#     dst_grudges = {"D/ST":[]}
#     for pos in playersWithGrudges.keys():
#         if pos in defensive_positions:
#             for player in playersWithGrudges[pos]:
#                 dst_grudges["D/ST"].append(player)
#     dsts = [(g[1], g[2]) for g in dst_grudges["D/ST"]]
#     dsts_temp = [(team[0], dsts.count(team), team[1], '', '', '') for team in set(dsts)]
#     dsts_sorted = sorted(dsts_temp, key=lambda x: x[1], reverse=True)[:3]
#     dst_grudges["D/ST"] = dsts_sorted
#     if dst_grudges["D/ST"]:
#         playersWithGrudges.update(dst_grudges)

# def display_grudges(position_type, positions):
#     """
#     Print out player grudges by position.

#     :param position_type: The print header for the output.
#     :type position_type: str
#     :param positions: The list of positions to print contents for.
#     :type positions: list
#     """
#     print(GREEN + position_type + RESET + "\n")
#     for pos in positions:
#         print(RED + f"{pos}" + RESET + "\n")
#         try:
#             players_at_position = playersWithGrudges[pos]
#         except:
#             print("None\n")
#             continue
#         # sort players by grudge length, always putting primary grudges first
#         players_at_position = sorted([(p[0], p[1], p[2], p[3], p[4], p[5], (1000 if p[2] == p[4] else 0) + len(p[3])) for p in players_at_position], key=lambda x: x[6], reverse=True)
#         for player_info in players_at_position:
#             name, curr_team, former_team, yrs_played, initial_team, fantasy_pos_rk, grudge_type_no = player_info
#             grudge_type = "grudge"
#             if initial_team == former_team:
#                 grudge_type = "primary grudge"
#             yrs_spent = len(yrs_played)
#             yrs_spent_str = "season"
#             if yrs_spent > 1:
#                 yrs_spent_str = "seasons"
#             print(BOLD + name + RESET + f" ({curr_team}) has a {grudge_type}" + RESET + f" against {former_team}.")
#             if pos != "D/ST":
#                 print(f"He spent {yrs_spent} {yrs_spent_str} with {former_team} {yrs_played}.")
#             if position_type == "FANTASY":
#                 if fantasy_pos_rk:
#                     if int(fantasy_pos_rk) <= 50:
#                         fantasy_pos_rk = GOLD + fantasy_pos_rk
#                     print(f"His position rank in fantasy this season is {fantasy_pos_rk}" + RESET + ".")
#             print()
#     print()

### MOVE TO EXTRA.PY
    #     if "-" in position:
    #         pos_list = position.split("-")
    #     else:
    #         pos_list = [position]
    #     for pos in pos_list:
    #         all_pos = fantasy_positions + defensive_positions + \
    #             offensive_line_positions + utility_positions
    #         if pos not in all_pos:
    #             pos = position_translator[pos]
    #         try:
    #             playersWithGrudges[pos].append((name, t1, t2, years_played, initial_team, fantasy_pos_rk))
    #         except:
    #             playersWithGrudges[pos] = []
    #             playersWithGrudges[pos].append((name, t1, t2, years_played, initial_team, fantasy_pos_rk))
    
    # matchupKey = t1+"-"+t2
    # playersWithGrudgesCopy = playersWithGrudges.copy()

# alphaName = ''.join(char for char in name if char.isalpha())
        # splitName = name.split(" ")
        # if len(splitName) > 2:
        #     splitName = splitName[:2]
        # if len(splitName) > 1:
        #     urlName = ''.join(char for char in splitName[1] if char.isalpha())[:4] + ''.join(char for char in splitName[0] if char.isalpha())[:2] + '00_2025'

# for day in days:
#     build_me.append()
#     for game in games:


# for matchup in nfl_schedule[int(week)-1]:
#     # day = matchup[0]
#     t1 = matchup[0]
#     t2 = matchup[1]
#     awayTeamKey = t1+"-"+t2
#     homeTeamKey = t2+"-"+t1
#     print("**MATCHUP**\n" + t1 + " @ " + t2 + "\n")
#     print(t1 + " Players With Grudges:")
#     for pos in final_positions:
#         if pos in grudgesByMatchup[awayTeamKey].keys():
#             print(pos + ": ", end="")
#             print(grudgesByMatchup[awayTeamKey][pos])
#     print()
#     print(t2 + " Players With Grudges:")
#     for pos in final_positions:
#         if pos in grudgesByMatchup[homeTeamKey].keys():
#             print(pos + ": ", end="") 
#             print(grudgesByMatchup[homeTeamKey][pos])
#     print()
#     print("\n")
# print()
# print(grudgesByMatchup)

##### 8-13 DEBUG
# print(teams)
# dst_grudges = count_dst_grudges()
# print("\n" + BOLD + "Players with Grudges:" + RESET + "\n")
# display_grudges("FANTASY", fantasy_positions)
# display_grudges("DEFENSE", defensive_positions)
# display_grudges("OFFENSIVE LINE", offensive_line_positions)
# display_grudges("UTILITY", utility_positions)