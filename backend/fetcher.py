# global/feed?siteAreaId=4869&page=1&records=10&lang=en

# global/details?lang=en&appItems=true&followItems=true&siteItems=true&featuredItems=true&allTeams=true

# edition/details?lang=en&edition=in&navigation=true&trendingMatches=true&keySeriesItems=true&sponsoredItems=true&promotedItems=true

# pages/match/scorecard?lang=en&seriesId={sid}&matchId={mid}

# edition/details?lang=en&edition=in&navigation=true&trendingMatches=true&keySeriesItems=true&sponsoredItems=true&promotedItems=true

# pages/match/home?lang=en&seriesId={sid}&matchId={mid}

# pages/match/smart-scorecard?lang=en&seriesId={sid}&matchId={mid}

# pages/match/report?lang=en&seriesId={sid}&matchId={mid}

# pages/match/commentary?lang=en&seriesId={sid}&matchId={mid}&sortDirection=DESC

# pages/match/comments?lang=en&seriesId={sid}&matchId={mid}&inningNumber=2&commentType=ALL&sortDirection=DESC&fromInningOver=14

# pages/match/statistics?lang=en&seriesId={sid}&matchId={mid}

# pages/match/overs?lang=en&seriesId={sid}&matchId={mid}

# pages/matches/current?lang=en&latest=true

import requests
import json
import time


class EFetcher:
    
    API_BASE_URL = "https://hs-consumer-api.espncricinfo.com/v1/"

    def __init__(self, mid:int, sid=1227837, scheidx=1):
        self.get_home_url = f"pages/match/home?lang=en&seriesId={sid}&matchId={mid}"
        self.get_scorecard_url = f"pages/match/scorecard?lang=en&seriesId={sid}&matchId={mid}"
        self.get_smartsorecard_url = f"pages/match/smart-scorecard?lang=en&seriesId={sid}&matchId={mid}"
        self.get_report_url = f"pages/match/report?lang=en&seriesId={sid}&matchId={mid}"
        self.get_commentary_url = f"pages/match/commentary?lang=en&seriesId={sid}&matchId={mid}&sortDirection=DESC"
        self.get_comments_url = f"pages/match/comments?lang=en&seriesId={sid}&matchId={mid}&commentType=ALL&sortDirection=DESC"
        self.get_stats_url = f"pages/match/statistics?lang=en&seriesId={sid}&matchId={mid}"
        self.get_overs_url = f"pages/match/overs?lang=en&seriesId={sid}&matchId={mid}"
        self.get_team_players_url = f"pages/match/team-players?lang=en&seriesId={sid}&matchId={mid}"
        self.get_matches_url = f'pages/matches/{["scheduled", "live", "result", "current"][scheidx]}?lang=en{["", "", "", "&latest=true"][scheidx]}'
        self.get_standings_url = f'pages/series/standings?lang=en&seriesId={sid}'

    def fetch_url(self, subdir: str):
        try:
            url = f"{self.API_BASE_URL}{subdir}"
            response = requests.get(url, stream=True)
            return response.json()
        except Exception as e:
            print(e)
            return -1
# sid=1327499
# mid=1327506
# a = EFetcher(mid, sid)
# data = a.fetch_url(a.get_home_url)
