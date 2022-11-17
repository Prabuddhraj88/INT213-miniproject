# import fetcher
import json
import matplotlib.pyplot as mp
import numpy as np
import io
from PIL import Image

class EParser:
    def __init__(self):
        ''

    def get_schedule(self, response, limit=10):
        schedules_container = []
        try:
            response = response["content"]["matches"]
        except Exception: response = response["matches"]
        for i in response:
            schedules_container.append(
                [
                    i["objectId"],
                    i["stage"],
                    i["state"],
                    i["season"],
                    i["title"],
                    i["coverage"],
                    i["startTime"],
                    i["statusText"],
                    i["tossWinnerTeamId"],
                    i["tossWinnerChoice"],
                    i["winnerTeamId"],
                    i["resultStatus"],
                    i["liveInning"],
                    [
                        i["series"]["objectId"],
                        i["series"]["longName"],
                        i["series"]["description"]
                    ],
                    i["ground"]["smallName"] if i["ground"] != None else None,
                    [
                        i["teams"][0]["team"]["longName"],
                        i["teams"][0]["team"]["primaryColor"],
                        i["teams"][0]["team"]["image"]["url"] if i["teams"][0]["team"]["image"] != None else None,
                        i["teams"][0]["isLive"],
                        i["teams"][0]["score"],
                        i["teams"][1]["team"]["longName"],
                        i["teams"][1]["team"]["primaryColor"],
                        i["teams"][1]["team"]["image"]["url"] if i["teams"][1]["team"]["image"] != None else None,
                        i["teams"][1]["isLive"],
                        i["teams"][1]["score"],
                        i["teams"][0]["team"]["id"],
                        i["teams"][1]["team"]["id"],
                    ],
                    i["format"]
                ]
            )
        return schedules_container

    def get_player(self, response, player_index:int, team_index:int):
        # response = self.efetcher.fetch_url(self.efetcher.get_scorecard_url)
        i=response["content"]["matchPlayers"]["teamPlayers"][team_index]
        team_data = i["team"]
        team_data_parsed = [
            team_data["name"],
            team_data["primaryColor"],
            team_data["image"]["url"]
        ]
        player_data = i["players"][player_index]
        player_data_parsed = [
            player_data["playerRoleType"],
            player_data["player"]["longName"],
            player_data["player"]["gender"],
            player_data["player"]["battingStyles"][0]  if player_data["player"]["battingStyles"] != [] else None,
            player_data["player"]["longBowlingStyles"][0] if player_data["player"]["longBowlingStyles"] != [] else None,
            player_data["player"]["image"]["url"],
            player_data["player"]["countryTeamId"],
            '-'.join(str(x) for x in player_data["player"]["dateOfBirth"].values()),
        ]
        return team_data_parsed, player_data_parsed 

    def get_best_players(self, response, team_index:int):
        i=response["content"]["matchPlayers"]["teamPlayers"][team_index]
        players_data = []
        data=i["bestBatsmen"]
        for bp_raw_data in data:
            player_data = [
                bp_raw_data["matches"],
                bp_raw_data["runs"],
                bp_raw_data["innings"],
                bp_raw_data["average"],
                bp_raw_data["notouts"],
                bp_raw_data["strikerate"],
                bp_raw_data["player"]["longName"],
                bp_raw_data["player"]["gender"],
                bp_raw_data["player"]["battingStyles"][0],
                bp_raw_data["player"]["longBowlingStyles"][0],
                bp_raw_data["player"]["image"]["url"],
                bp_raw_data["player"]["countryTeamId"],
                '-'.join(str(x) for x in bp_raw_data["player"]["dateOfBirth"].values()),
            ]
            players_data.append(player_data)
        data=i["bestBowlers"]
        for bp_raw_data in data:
            player_data = [
                bp_raw_data["matches"],
                bp_raw_data["wickets"],
                bp_raw_data["innings"],
                bp_raw_data["average"],
                bp_raw_data["economy"],
                bp_raw_data["conceded"],
                bp_raw_data["balls"],
                bp_raw_data["player"]["longName"],
                bp_raw_data["player"]["gender"],
                bp_raw_data["player"]["battingStyles"][0],
                bp_raw_data["player"]["longBowlingStyles"][0],
                bp_raw_data["player"]["image"]["url"],
                bp_raw_data["player"]["countryTeamId"],
                '-'.join(str(x) for x in bp_raw_data["player"]["dateOfBirth"].values()),
            ]
            players_data.append(player_data)
        return players_data

    def get_scorecard(self, response):
        i = response["match"]
        j = response["content"]
        match_details = [
            i["objectId"],
            i["stage"],
            i["state"],
            i["season"],
            i["title"],
            i["coverage"],
            i["startTime"],
            i["statusText"],
            i["tossWinnerTeamId"],
            i["tossWinnerChoice"],
            i["winnerTeamId"],
            i["resultStatus"],
            i["liveInning"],
            [
                i["series"]["objectId"],
                i["series"]["longName"],
                i["series"]["description"]
            ],
            i["ground"]["longName"],
            [
                i["teams"][0]["team"]["longName"],
                i["teams"][0]["team"]["primaryColor"],
                i["teams"][0]["team"]["image"]["url"] if i["teams"][0]["team"]["image"] != None else None,
                i["teams"][0]["isLive"],
                i["teams"][0]["score"],
                i["teams"][1]["team"]["longName"],
                i["teams"][1]["team"]["primaryColor"],
                i["teams"][1]["team"]["image"]["url"] if i["teams"][1]["team"]["image"] != None else None,
                i["teams"][1]["isLive"],
                i["teams"][1]["score"],
            ],
            i["format"]
        ]
        innings = j["scorecard"]["innings"]
        innings_container = []
        for k in innings:
            team_details = [
                k["inningNumber"],
                [
                    k["team"]["longName"],
                    k["team"]["primaryColor"],
                    k["team"]["image"]["url"] if k["team"]["image"] != None else None,
                ],
                k["isBatted"],
                k["runs"],
                k["wickets"],
                k["lead"],
                k["target"],
                k["overs"],
                k["balls"],
                k["totalOvers"],
                k["extras"],
                k["byes"],
                k["legbyes"],
                k["wides"],
                k["noballs"],
                k["penalties"],
            ]
            players_details = {
                "batsmen": [],
                "bowlers": []
            }
            for batsman in k["inningBatsmen"]:
                players_details["batsmen"].append([
                    batsman["playerRoleType"],
                    batsman["player"]["longName"],
                    batsman["battedType"],
                    batsman["runs"],
                    batsman["balls"],
                    batsman["fours"],
                    batsman["sixes"],
                    batsman["strikerate"],
                    batsman["isOut"],
                    batsman["dismissalText"]["long"] if batsman["dismissalText"] != None else None
                ])
            for bowler in k["inningBowlers"]:
                players_details["bowlers"].append([
                    bowler["player"]["longName"],
                    bowler["bowledType"],
                    bowler["overs"],
                    bowler["maidens"],
                    bowler["conceded"],
                    bowler["wickets"],
                    bowler["economy"],
                    bowler["dots"],
                    bowler["fours"],
                    bowler["sixes"],
                    bowler["wides"],
                    bowler["noballs"]
                ])
            innings_container.append([team_details, players_details])
        return innings_container

    def get_parnership_graph(self, response, inning_index:int):
        try:inning = response["content"]["inningsPerformance"]["innings"][inning_index]
        except IndexError: return None
        state = response["match"]["state"]
        team_name = inning["team"]["name"]
        team_color = inning["team"]["primaryColor"]
        team_logo = inning["team"]["image"]["url"]
        partnerships = inning["inningPartnerships"]
        x, runs, balls = [], [], []
        for partnership in partnerships:
            x.append(partnership["player1"]["fieldingName"]+"\n"+partnership["player2"]["fieldingName"])
            runs.append(partnership["runs"])
            balls.append(partnership["balls"])
        x_pos = [i for i, _ in enumerate(x)]
        mp.bar(x_pos, runs, color=team_color, width=0.7)
        mp.xlabel("Partners")
        mp.ylabel("Runs")
        mp.title(f"Partnerships: {team_name}")
        mp.xticks(x_pos, x, fontsize=7)
        r = sorted(runs)
        highest_score = int(r[len(runs)-1])
        mp.yticks(np.arange(0, highest_score+10, step=15))
        for i in range(len(runs)):
            mp.annotate(f'{runs[i]} in {balls[i]}', (x_pos[i]-0.3, runs[i]+1), fontsize=8)
        fig = mp.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        mp.cla()
        return buf, state, team_name, team_color, team_logo

    def get_fall_of_wickets(self, response, inning_index:int):
        try:inning = response["content"]["inningsPerformance"]["innings"][inning_index]
        except IndexError: return None
        state = response["match"]["state"]
        team_name = inning["team"]["name"]
        team_color = inning["team"]["primaryColor"]
        team_logo = inning["team"]["image"]["url"]
        inningWickets = inning["inningWickets"]
        x, o, s = [], [], []
        for wicket in inningWickets:
            x.append(wicket["player"]["fieldingName"])
            o.append(float(wicket['fowOvers']))
            s.append(int(wicket['fowRuns']))
        mp.xticks(np.arange(0, int(o[len(o)-1]+100), step=5))
        mp.yticks(np.arange(0, int(s[len(s)-1]+100), step=15))
        mp.title('Fall of wicket: '+team_name, fontsize=14)
        mp.xlabel('Overs', fontsize=14)
        mp.ylabel('Runs', fontsize=14)
        mp.plot(o, s, color='red', marker='o', linewidth=3, markerfacecolor='red', markersize=8, label='Wickets')
        for i in range(len(o)):
            mp.annotate(x[i] + f'\n({s[i]})-{o[i]})', (o[i]+2, s[i]-2), fontsize=7)
        mp.plot(o, s, color=team_color, label='Runs')
        mp.legend(loc='lower right')
        fig = mp.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        mp.cla()
        return buf, state, team_name, team_color, team_logo

    def get_overs(self, response, inning_index:int):
        inning = response["content"]["inningOvers"][inning_index]
        overs_container =  []
        for i in inning["stats"]:
            overs_container.append([
                i["overRuns"],
                i["overWickets"],
                i["bowlers"][0]["longName"]
            ])
        return overs_container
        
    def get_comments(self, response):
        comment_container = []
        for i in response["comments"]:
            comment_container.append([
                i['inningNumber'],
                i['oversActual'],
                i['isFour'],
                i['isSix'],
                i['isWicket'],
                i['dismissalType'],
                i['byes'],
                i['legbyes'],
                i['wides'],
                i['noballs'],
                i['title'],
                i['dismissalText'],
                i['commentTextItems'][0]['html'],
                i['commentPostTextItems'][0]['html'] if i['commentPostTextItems'] != None else None,
            ])
        return comment_container

    def get_home(self, response):
        i = response["match"]
        match_container = [
            i["objectId"],
            i["stage"],
            i["state"],
            i["season"],
            i["title"],
            i["coverage"],
            i["startTime"],
            i["statusText"],
            i["tossWinnerTeamId"],
            i["tossWinnerChoice"],
            i["winnerTeamId"],
            i["resultStatus"],
            i["liveInning"],
            [
                i["series"]["objectId"],
                i["series"]["longName"],
                i["series"]["description"]
            ],
            i["ground"]["longName"],
            [
                i["teams"][0]["team"]["longName"],
                i["teams"][0]["team"]["primaryColor"],
                i["teams"][0]["team"]["image"]["url"] if i["teams"][0]["team"]["image"] != None else None,
                i["teams"][0]["isLive"],
                i["teams"][0]["score"],
                i["teams"][1]["team"]["longName"],
                i["teams"][1]["team"]["primaryColor"],
                i["teams"][1]["team"]["image"]["url"] if i["teams"][1]["team"]["image"] != None else None,
                i["teams"][1]["isLive"],
                i["teams"][1]["score"],
            ],
            i["format"]
        ]
        try:
            comments = response["content"].get("recentBallCommentary", None).get("ballComments", None)
        except AttributeError:
            comments = None
        comment_container = []
        if comments != None:
            for i in comments:
                comment_container.append([
                    i['inningNumber'],
                    i['oversActual'],
                    i['isFour'],
                    i['isSix'],
                    i['isWicket'],
                    i['title'],
                    i['dismissalText'],
                    i['commentTextItems'][0]['html'] if i['commentTextItems']!= None and i['commentTextItems'][0]!= None else None,
                    i['commentPostTextItems'][0].get('html', None) if i['commentPostTextItems'] != None and i['commentPostTextItems'][0]!=None else None
                ])
            
        players_container = []
        try:
            teamPlayers=response["content"]["matchPlayers"]["teamPlayers"]
            for i in teamPlayers:
                team_data = i["team"]
                team_data_parsed = [
                    team_data["name"],
                    team_data["primaryColor"],
                    team_data["image"]["url"]
                ]
                players_data = i["players"]
                player_data_parsed = []
                for player_data in players_data:
                    player_data_parsed.append([
                        player_data["playerRoleType"],
                        player_data["player"]["longName"],
                        player_data["player"]["gender"],
                        player_data["player"]["battingStyles"][0]  if player_data["player"]["battingStyles"] != [] else None,
                        player_data["player"]["longBowlingStyles"][0] if player_data["player"]["longBowlingStyles"] != [] else None,
                        player_data["player"]["image"]["url"] if player_data["player"]["image"] != None else None,
                    ])
                players_container.append([team_data_parsed, player_data_parsed])
        except TypeError: pass
        innings_container = []
        try:
            innings = response["content"]["scorecardSummary"]["innings"]
            for k in innings:
                team_details = [
                    k["inningNumber"],
                    [
                        k["team"]["longName"],
                        k["team"]["primaryColor"],
                        k["team"]["image"]["url"] if k["team"]["image"] != None else None,
                    ],
                    k["isBatted"],
                    k["runs"],
                    k["wickets"],
                    k["lead"],
                    k["target"],
                    k["overs"],
                    k["balls"],
                    k["totalOvers"],
                    k["extras"],
                    k["byes"],
                    k["legbyes"],
                    k["wides"],
                    k["noballs"],
                    k["penalties"],
                ]
                players_details = {
                    "batsmen": [],
                    "bowlers": []
                }
                for batsman in k["inningBatsmen"]:
                    players_details["batsmen"].append([
                        batsman["playerRoleType"],
                        batsman["player"]["longName"],
                        batsman["battedType"],
                        batsman["runs"],
                        batsman["balls"],
                        batsman["fours"],
                        batsman["sixes"],
                        batsman["strikerate"],
                        batsman["isOut"],
                        batsman["dismissalText"]["long"] if batsman["dismissalText"] != None else None
                    ])
                for bowler in k["inningBowlers"]:
                    players_details["bowlers"].append([
                        bowler["player"]["longName"],
                        bowler["bowledType"],
                        bowler["overs"],
                        bowler["maidens"],
                        bowler["conceded"],
                        bowler["wickets"],
                        bowler["economy"],
                        bowler["dots"],
                        bowler["fours"],
                        bowler["sixes"],
                        bowler["wides"],
                        bowler["noballs"]
                    ])
                innings_container.append([team_details, players_details])
        except TypeError as e: 
            pass
        i=response["content"]["bestPerformance"]
        players_data = []
        if i != None:
            data=i["batsmen"]
            for bp_raw_data in data:
                player_data = [
                    bp_raw_data["runs"],
                    bp_raw_data["balls"],
                    bp_raw_data["fours"],
                    bp_raw_data["sixes"],
                    bp_raw_data["shot"],
                    bp_raw_data["wagonData"],
                    bp_raw_data["strikerate"],
                    bp_raw_data["player"]["longName"],
                    bp_raw_data["player"]["gender"],
                    bp_raw_data["player"]["battingStyles"][0] if bp_raw_data["player"]["battingStyles"] != [] else None,
                    bp_raw_data["player"]["longBowlingStyles"][0] if bp_raw_data["player"]["longBowlingStyles"] != [] else None,
                    None if bp_raw_data["player"]["image"]==None else bp_raw_data["player"]["image"]["url"],
                ]
                players_data.append(player_data)

            data=i["bowlers"]
            for bp_raw_data in data:
                player_data = [
                    bp_raw_data["wickets"],
                    bp_raw_data["balls"],
                    bp_raw_data["conceded"],
                    bp_raw_data["lhbPitchMap"],
                    bp_raw_data["rhbPitchMap"],
                    bp_raw_data["economy"],
                    bp_raw_data["player"]["longName"],
                    bp_raw_data["player"]["gender"],
                    bp_raw_data["player"]["battingStyles"][0] if bp_raw_data["player"]["battingStyles"] != [] else None,
                    bp_raw_data["player"]["longBowlingStyles"][0] if bp_raw_data["player"]["longBowlingStyles"] != [] else None,
                    None if bp_raw_data["player"]["image"]==None else bp_raw_data["player"]["image"]["url"],
                ]
                players_data.append(player_data)
        return match_container, comment_container, players_container, innings_container, players_data

    def get_standings(self, response):
        return response

# sid=1327499
# mid=1327506
# parser = EParser()
# efetcher = fetcher.EFetcher(mid)
# response = efetcher.fetch_url(efetcher.get_standings_url)
# # print(json.dumps(response))

# print(json.dumps(parser.get_standings(response)))