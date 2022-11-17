from tkinter import *
import backend.fetcher as fetcher
import backend.parser as parser
from frontend.embedGenerator import EmbedGenerator

class StateApp:
    def __init__(self, root):
        
        self.root = root
        
        # setting series id null by default
        self.sid=None
        # setting match id null by default
        self.mid=None

        # initializing parser object
        self.parser = parser.EParser()

        # creating central frame
        self.centralFrame = Frame(self.root, height=260)
    
        # initalizing embed generator object
        self.embedEngine = EmbedGenerator()

    def initiator(self): # initiate schedules module
        # container to store data for initial state
        data_con = {}

        # fetching data for all 3 options embedding
        for i in range(0, 3):
            efetcher = fetcher.EFetcher(self.mid, self.sid, i)
            response = efetcher.fetch_url(efetcher.get_matches_url)
            data_con[[ "Upcoming", "Live", "Result"][i]] = self.parser.get_schedule(response)

        efetcher = fetcher.EFetcher(self.mid, self.sid, 3)
        response1 = self.parser.get_schedule(efetcher.fetch_url(efetcher.get_matches_url))
        # embedding recents in central frame
        self.embedEngine.embed_recents(self, self.centralFrame, self.root, response1).grid(row=0, column=0, sticky="ew")
        # embedding matches in central frame
        self.embedEngine.embed_matches(self, self.centralFrame, data_con).grid(row=1, column=0, sticky="news")
        return self.root
    
    def add_home(self, mid:int, sid:int):
        self.sid = sid
        self.mid = mid
        efetcher = fetcher.EFetcher(self.mid, self.sid)
        response = efetcher.fetch_url(efetcher.get_home_url)
        parsed_data = self.parser.get_home(response)
        self.embedEngine.embed_home(self.centralFrame, parsed_data)

    def add_scorecard(self, mid:int, sid:int):
        self.sid = sid
        self.mid = mid
        efetcher = fetcher.EFetcher(self.mid, self.sid)
        response = efetcher.fetch_url(efetcher.get_scorecard_url)
        parsed_data = self.parser.get_scorecard(response)
        self.embedEngine.embed_scorecard(self.centralFrame, response)

    def add_commentary(self, mid:int, sid:int):
        self.sid = sid
        self.mid = mid
        efetcher = fetcher.EFetcher(self.mid, self.sid)
        response = efetcher.fetch_url(efetcher.get_commentary_url)
        parsed_data = self.parser.get_comments(response)
        self.embedEngine.embed_commentary(self.centralFrame, parsed_data)

    def add_standing(self, mid:int, sid:int):
        self.sid = sid
        self.mid = mid
        efetcher = fetcher.EFetcher(self.mid, self.sid)
        response = efetcher.fetch_url(efetcher.get_stats_url)
        parsed_data = self.parser.get_standings(response)
        self.embedEngine.embed_commentary(self.centralFrame, parsed_data)

    def add_player(self, mid:int, sid:int, pidx:int):
        self.sid = sid
        self.mid = mid
        efetcher = fetcher.EFetcher(self.mid, self.sid)
        response = efetcher.fetch_url(efetcher.get_stats_url)
        parsed_data = self.parser.get_standings(response)
        self.embedEngine.embed_commentary(self.centralFrame, parsed_data)
