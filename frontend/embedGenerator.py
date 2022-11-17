# -*- coding: utf-8 -*-
from functools import partial
import requests
from tkinter import ttk
from tkinter import *
from frontend.doubleScrolledFrame import DoubleScrolledFrame
from frontend.constants import *
from PIL import ImageTk, Image
import numpy
import math

class EmbedGenerator:

    # function to take a frame and delete all the widgets inside it
    ## completed
    def clearFrame(self, frame):
        # destroy all widgets from frame
        for widget in frame.winfo_children():
            widget.destroy()

    ## completed
    def embed_recents(self, obj, centralFrame, parent, data):
        recent_container = DoubleScrolledFrame(parent, type_=1, borderwidth=2, background="gray", height=220, width=windowWidth)
        col_idx = 2
        for i in data[:15]:
            # setting image url by default to no image url
            valid_url = NO_IMAGE_URL
            img = Image.open(open(valid_url, "rb")).resize((50, 50))
            # setting frame color by default to grey
            frameColor = 'grey'
            
            if i[15][1] != None: # team color
                # changing frame color to team color if team color is not null
                frameColor = i[15][1]

            # head title which contains match state, series name, macth name, place       
            headTitle = f'{i[2]} · {i[13][1]} · {i[16]} · {i[14]}'
            
            if i[15][2] != None: # team image url
                # changing frame image1 to team image if team image is not null
                valid_url = f'{BASE_IMAGE_URL}{i[15][2]}'            
                # fetching image with requests and storing it as PIL Image object
                img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
            
            icon = ImageTk.PhotoImage(img)

            # creating item frame object to contain match details
            itemBox = Frame(recent_container, highlightbackground=frameColor, highlightthickness=2)

            Label(itemBox, text=headTitle, anchor="w").grid(padx=10, pady=10, sticky="ew", row=0, column=1)

            iconLabel = Label(itemBox)
            iconLabel.image = icon
            iconLabel.configure(image= icon)
            iconLabel.grid(sticky='ew', row = 1, column=0, padx=10)
            scoreTitle = i[15][0]
            
            if i[15][3]: scoreTitle += "*"

            Label(itemBox, text=f'{scoreTitle} ({i[15][4]})').grid(row = 1, column=1)

            # comments implies same as team 1 for team 2
            valid_url = NO_IMAGE_URL
            img = Image.open(open(valid_url, "rb")).resize((50, 50))
            if i[15][7] != None:
                valid_url = f'{BASE_IMAGE_URL}{i[15][7]}'
                img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
            
            icon = ImageTk.PhotoImage(img)

            iconLabel2 = Label(itemBox)
            iconLabel2.image = icon
            iconLabel2.configure(image= icon)
            iconLabel2.grid(sticky='ew', row = 2, column=0, padx=10)
            scoreTitle = i[15][5]
            
            if i[15][8]: scoreTitle += "*"

            Label(itemBox, text=f'{scoreTitle} ({i[15][9]})').grid(row = 2, column=1)
            Label(itemBox, text=i[7], foreground="grey").grid(row=3, column=1)
            Button(itemBox, text="View", command=partial(obj.add_home, i[0], i[13][0])).grid(row=4, column=2, padx=10)
            itemBox.grid(padx=15, sticky='ns', row=0, column=col_idx)
            col_idx+=2

        return recent_container

    ## completed
    def embed_matches(self, obj, centralFrame, data_con):
        self.clearFrame(centralFrame)
        tabControl = ttk.Notebook(centralFrame, width=windowWidth)
        for k in data_con:
            liveTab = DoubleScrolledFrame(tabControl, type_=1, name=k.lower(), borderwidth=2, background="gray", height=410, width=windowWidth)
            data = data_con[k]
            tabControl.add(liveTab, text = k)
            col_idx = 2
            for i in data[:15]:
                valid_url = NO_IMAGE_URL
                img = Image.open(open(valid_url, "rb")).resize((50, 50))
                frameColor = 'grey'
                
                if i[15][1] != None: # team color
                    frameColor = i[15][1]
                state = i[2]
                seriesName = i[13][1]
                format_ = i[16]
                venue = i[14]
                
                if i[15][2] != None: # team image url
                    valid_url = f'{BASE_IMAGE_URL}{i[15][2]}'
                    img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
                
                icon = ImageTk.PhotoImage(img)

                itemBox = Frame(liveTab, highlightbackground=frameColor, highlightthickness=2, width=windowWidth)
                stateColor = colors[["LIVE", "PRE", "POST"].index(i[2])]
                
                Label(itemBox, text=state, background=stateColor, foreground="white")\
                .grid(padx=10, pady=10, sticky="ew", row=0, column=0)

                Label(itemBox, text=f'Series Name: {seriesName}', anchor="w", background="grey", foreground="white")\
                .grid(padx=10, pady=10, sticky="ew", row=0, column=1)
                
                Label(itemBox, text=f'Format: {format_}', anchor="w", background="grey", foreground="white")\
                .grid(padx=10, pady=10, sticky="ew", row=0, column=2)

                Label(itemBox, text=f'Venue: {venue}', anchor="w", background="grey", foreground="white")\
                .grid(padx=10, pady=10, sticky="ew", row=0, column=3)
                
                Label(itemBox, text=f'Stage: {i[1]}', anchor="w")\
                .grid(padx=10, pady=10, sticky="ew", row=1, column=0)

                Label(itemBox, text=f'Season: {i[3]}', anchor="w")\
                .grid(padx=10, pady=10, sticky="ew", row=1, column=1)

                Label(itemBox, text=f'Title: {i[4]}', anchor="w")\
                .grid(padx=10, pady=10, sticky="ew", row=1, column=2)

                Label(itemBox, text=f"Start Time: {i[6].replace('T', ' ').replace('.000Z', '')}", anchor="w")\
                .grid(padx=10, pady=10, sticky="ew", row=1, column=3)
                
                try:
                    chose = ["chose to Bat", "chose to Field"][int(i[9])-1]
                except TypeError: chose = "None"        

                if i[15].index(i[8]) == 10 and i[8]!=None:
                    Label(itemBox, text=f'Toss Winner: {i[15][0]} - {chose}', anchor="w")\
                    .grid(padx=10, pady=10, sticky="ew", row=2, column=0)
                
                if i[15].index(i[8]) == 11 and i[8]!=None:
                    Label(itemBox, text=f'Toss Winner: {i[15][5]} - {chose}', anchor="w")\
                    .grid(padx=10, pady=10, sticky="ew", row=2, column=0)
                
                else:
                    Label(itemBox, text=f'Toss Winner: None', anchor="w").grid(padx=10, pady=10, sticky="ew", row=2, column=0)
                
                if i[10]!=None and i[15].index(i[10]) == 10:
                    winner = i[15][0]
                if i[10]!=None and i[15].index(i[10]) == 11:
                    winner = i[15][5]
                else: winner = "None"

                Label(itemBox, text=f'Winner: {winner}', anchor="w")\
                .grid(padx=10, pady=10, sticky="ew", row=2, column=1)

                scoreTitle = i[15][0]
                if i[15][3]: scoreTitle += "*"

                iconLabel = Label(itemBox)
                iconLabel.image = icon
                iconLabel.configure(image = icon, text=f'{scoreTitle} ({i[15][4]})', compound="left")
                iconLabel.grid(sticky='ew', row = 3, column=0, padx=10)

                # for team 2
                valid_url = NO_IMAGE_URL
                img = Image.open(open(valid_url, "rb")).resize((50, 50))
                if i[15][7] != None:
                    valid_url = f'{BASE_IMAGE_URL}{i[15][7]}'
                    img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
                    
                scoreTitle = i[15][5]
                
                if i[15][8]: scoreTitle += "*"

                icon = ImageTk.PhotoImage(img)

                iconLabel2 = Label(itemBox)
                iconLabel2.image = icon
                iconLabel2.configure(image = icon, text=f'{scoreTitle} ({i[15][9]})', compound="left")
                iconLabel2.grid(sticky='ew', row = 3, column=2, padx=10)
                
                
                Label(itemBox, text=i[7], foreground="grey")\
                    .grid(row=4, column=1, pady=10)
                
                if i[5] == "Y":
                    Button(itemBox, text="Details", command=partial(obj.add_home, i[0], i[13][0]))\
                    .grid(row=4, column=3, padx=10)

                itemBox.grid(padx=15, sticky='news', row=col_idx, column=2)
                col_idx+=1
        tabControl.pack(expand = 1, fill="x")
        return centralFrame

    ## on it
    def embed_home(self, mainFrame, data_con):
        self.clearFrame(mainFrame)
        mainFrame = DoubleScrolledFrame(mainFrame, type_=1, borderwidth=2, background="gray", height=410, width=windowWidth)
        
        ## match details section
        i = data_con[0]
        valid_url = NO_IMAGE_URL
        img = Image.open(open(valid_url, "rb")).resize((50, 50))
        frameColor = 'grey'
        
        if i[15][1] != None: # team color
            frameColor = i[15][1]
        state = i[2]
        seriesName = i[13][1]
        format_ = i[16]
        venue = i[14]
        
        if i[15][2] != None: # team image url
            valid_url = f'{BASE_IMAGE_URL}{i[15][2]}'
            img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
        
        icon = ImageTk.PhotoImage(img)
        itemBox = LabelFrame(mainFrame, text="Match Details", highlightbackground=frameColor, width=windowWidth)
        # itemBox = Frame(liveTab, highlightbackground=frameColor, highlightthickness=2, width=windowWidth)
        stateColor = colors[["LIVE", "PRE", "POST"].index(i[2])]
        
        Label(itemBox, text=state, background=stateColor, foreground="white")\
        .grid(padx=10, pady=10, sticky="ew", row=0, column=0)

        Label(itemBox, text=f'Series Name: {seriesName}', anchor="w", background="grey", foreground="white")\
        .grid(padx=10, pady=10, sticky="ew", row=0, column=1)
        
        Label(itemBox, text=f'Format: {format_}', anchor="w", background="grey", foreground="white")\
        .grid(padx=10, pady=10, sticky="ew", row=0, column=2)

        Label(itemBox, text=f'Venue: {venue}', anchor="w", background="grey", foreground="white")\
        .grid(padx=10, pady=10, sticky="ew", row=0, column=3)
        
        Label(itemBox, text=f'Stage: {i[1]}', anchor="w")\
        .grid(padx=10, pady=10, sticky="ew", row=1, column=0)

        Label(itemBox, text=f'Season: {i[3]}', anchor="w")\
        .grid(padx=10, pady=10, sticky="ew", row=1, column=1)

        Label(itemBox, text=f'Title: {i[4]}', anchor="w")\
        .grid(padx=10, pady=10, sticky="ew", row=1, column=2)

        Label(itemBox, text=f"Start Time: {i[6].replace('T', ' ').replace('.000Z', '')}", anchor="w")\
        .grid(padx=10, pady=10, sticky="ew", row=1, column=3)
        
        try:
            chose = ["chose to Bat", "chose to Field"][int(i[9])-1]
        except TypeError: chose = "None"        

        if i[8]!=None and i[8] in i[15] and i[15].index(i[8]) == 10:
            Label(itemBox, text=f'Toss Winner: {i[15][0]} - {chose}', anchor="w")\
            .grid(padx=10, pady=10, sticky="ew", row=2, column=0)
        
        if i[8]!=None and i[8] in i[15] and i[15].index(i[8]) == 11:
            Label(itemBox, text=f'Toss Winner: {i[15][5]} - {chose}', anchor="w")\
            .grid(padx=10, pady=10, sticky="ew", row=2, column=0)
        
        else:
            Label(itemBox, text=f'Toss Winner: None', anchor="w").grid(padx=10, pady=10, sticky="ew", row=2, column=0)
        try:
            if i[10]!=None and i[15].index(i[10]) == 10:
                winner = i[15][0]
            if i[10]!=None and i[15].index(i[10]) == 11:
                winner = i[15][5]
            else: winner = "None"
        except ValueError: winner = "None"
        Label(itemBox, text=f'Winner: {winner}', anchor="w")\
        .grid(padx=10, pady=10, sticky="ew", row=2, column=1)

        scoreTitle = i[15][0]
        if i[15][3]: scoreTitle += "*"

        iconLabel = Label(itemBox)
        iconLabel.image = icon
        iconLabel.configure(image = icon, text=f'{scoreTitle} ({i[15][4]})', compound="left")
        iconLabel.grid(sticky='ew', row = 3, column=0, padx=10)

        # for team 2
        valid_url = NO_IMAGE_URL
        img = Image.open(open(valid_url, "rb")).resize((50, 50))
        if i[15][7] != None:
            valid_url = f'{BASE_IMAGE_URL}{i[15][7]}'
            img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))
            
        scoreTitle = i[15][5]
        
        if i[15][8]: scoreTitle += "*"

        icon = ImageTk.PhotoImage(img)

        iconLabel2 = Label(itemBox)
        iconLabel2.image = icon
        iconLabel2.configure(image = icon, text=f'{scoreTitle} ({i[15][9]})', compound="left")
        iconLabel2.grid(sticky='ew', row = 3, column=2, padx=10)
        
        
        Label(itemBox, text=i[7], foreground="grey")\
            .grid(row=4, column=1, pady=10)
        itemBox.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        
        ## innings
        inningFrame = LabelFrame(mainFrame, labelanchor='n', text="Innings", highlightbackground=frameColor, width=windowWidth, background="white", font={"Arial", 24})
        i = data_con[3]
        if i != [] and i != None:
            for ridx, innTeam in enumerate(i):
                innTeamData, innPlayingData = innTeam
                
                inningTeamFrame = LabelFrame(inningFrame, text=f"{innTeamData[1][0]} - {innTeamData[0]} ({['On the way', 'Ended'][innTeamData[2]]})", font={"Arial", 20}, background=innTeamData[1][1], width=windowWidth)
                tFrame = Frame(inningTeamFrame, borderwidth=2, background="gray")
                Label(tFrame, text=f"Score: {innTeamData[3]}/{innTeamData[4]}", anchor="w", background="grey", foreground="white")\
                    .grid(row=0, column=0, padx=10, pady=10)
                Label(tFrame, text=f"Overs: {innTeamData[7]}/{innTeamData[9]}", anchor="w", background="grey", foreground="white")\
                    .grid(row=0, column=1, padx=10, pady=10)
                Label(tFrame, text=f"Extras: {innTeamData[10]}", anchor="w", background="grey", foreground="white")\
                    .grid(row=0, column=2, padx=10, pady=10)
                Label(tFrame, text=f"Penalties: {innTeamData[15]}", anchor="w", background="grey", foreground="white")\
                    .grid(row=0, column=3, padx=10, pady=10)
                tFrame.grid(row=0, column=0, padx=10, pady=10)

                batData, bowlData = innPlayingData.values()
                batsInnFrame = LabelFrame(inningTeamFrame, text=f"{list(innPlayingData.keys())[0].capitalize()}", width=windowWidth/4)
                opts = {'yes': '', 'no': '*'}
                for btdidx, btd in enumerate(batData):
                    btdsFrame = Frame(batsInnFrame, borderwidth=2, highlightthickness=3, background="#ecb0bc")
                    Label(btdsFrame, text=f"{btd[1]} ({btd[0]}){opts[btd[2]]}", font={"Arial", 15}, anchor="w", background="#059ea1", foreground="white")\
                        .grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                    Label(btdsFrame, text=f"Runs: {btd[3]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                    Label(btdsFrame, text=f"Balls: {btd[4]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=1, padx=10, pady=10, sticky="ew")
                    Label(btdsFrame, text=f"Fours: {btd[5]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=2, padx=10, pady=10, sticky="ew")
                    Label(btdsFrame, text=f"Sixes: {btd[6]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=2, column=0, padx=10, pady=10, sticky="ew")
                    Label(btdsFrame, text=f"Strike Rate: {btd[7]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=2, column=1, padx=10, pady=10, sticky="ew")
                    if btd[8]:
                        Label(btdsFrame, text=btd[9], anchor="w", background="#f64847", foreground="white")\
                            .grid(row=3, column=0, padx=10, pady=10, sticky="ew")
                    btdsFrame.grid(row=0, column=btdidx, padx=10, pady=10, sticky="news")
                batsInnFrame.grid(row=1, column=0, padx=10, pady=10, sticky="news")

                bowlInnFrame = LabelFrame(inningTeamFrame, text=f"{list(innPlayingData.keys())[1].capitalize()}", width=windowWidth, font={"Arial", 20})
                
                for bldidx, bld in enumerate(bowlData):
                    bldsFrame = Frame(bowlInnFrame, borderwidth=2, highlightthickness=3, background="#ecb0bc")
                    Label(bldsFrame, text=f"{bld[0]} {opts[bld[1]]}", font={"Arial", 15}, anchor="w", background="#059ea1", foreground="white")\
                        .grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                    Label(bldsFrame, text=f"Wickets: {bld[5]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                    Label(bldsFrame, text=f"Overs: {bld[2]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=1, padx=10, pady=10, sticky="ew")
                    Label(bldsFrame, text=f"Runs: {bld[4]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=1, column=2, padx=10, pady=10, sticky="ew")
                    Label(bldsFrame, text=f"Maidens: {bld[3]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=2, column=0, padx=10, pady=10, sticky="ew")
                    Label(bldsFrame, text=f"Economy: {bld[6]}", anchor="w", background="#ebb595", foreground="white")\
                        .grid(row=2, column=1, padx=10, pady=10, sticky="ew")
                    bldsFrame.grid(row=0, column=bldidx, padx=10, pady=10, sticky="news")

                bowlInnFrame.grid(row=2, column=0, padx=10, pady=10, sticky="news")
                inningTeamFrame.grid(row=ridx, column=0, padx=10, pady=10, sticky="news")
        
        else: 
            Label(inningFrame, text="Innings detail detail not available.", foreground="gray").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        inningFrame.grid(row=1, column=0, padx=10, pady=10, sticky="news")

        ## commentary
        commFrame = LabelFrame(mainFrame, text="Commentary", highlightbackground=frameColor, width=windowWidth)
        comments = data_con[1]
        if comments != [] and comments != None:
            for ridx, comment in enumerate(comments):
                commentFrame = LabelFrame(commFrame, text=f"{comment[1]} - {cleanHTML(comment[5])}", font={"Arial", 12})
                superTitle = "N"
                superTitleColor = "#87CEEB"
                if comment[2]: 
                    superTitle = "4"
                    superTitleColor = "blue"
                if comment[3]: 
                    superTitle = "6"
                    superTitleColor = "Purple"
                if comment[4]:
                    superTitle = "W"
                    superTitleColor = "black"
                commDesc = ""
                if comment[7] != None:
                    commDesc += f"{cleanHTML(comment[7])}"
                if comment[8] != None:
                    commDesc += f"\n{cleanHTML(comment[8])}"
                
                Label(commentFrame, text=superTitle, foreground="white", background=superTitleColor, font=("Arial", 15))\
                .grid(row=0, column=0, padx=10, pady=10)
                
                Label(commentFrame, text=commDesc, wraplength=1500)\
                .grid(row=0, column=1, padx=10, pady=10)
                

                commentFrame.grid(row=ridx, column=0, padx=10, pady=10, sticky="ew")
        else: 
            Label(commFrame, text="No commentary available.", foreground="gray").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        commFrame.grid(row=2, column=0, padx=10, pady=10, sticky="news")

        ## teams
        teamFrame = LabelFrame(mainFrame, text="Teams", highlightbackground=frameColor, width=windowWidth, font={"Arial", 20})
        i = data_con[2]
        if i != [] and i != None:
            for ridx, teamData in enumerate(i):
                frameColor = 'grey'
                if teamData[0][1] != None:
                    frameColor = teamData[0][1]
                sinTeamFrame = LabelFrame(teamFrame, text=teamData[0][0], highlightbackground=frameColor, background="white", width=windowWidth)
                playerData = teamData[1]
                for pcidx, player_chunk in enumerate(numpy.array_split(playerData, math.ceil(len(playerData)/3))):
                    for pidx, player in enumerate(player_chunk):
                        playerFrame = Frame(sinTeamFrame, width=windowWidth, borderwidth=3, background="#305a7b")
                        valid_url = NO_IMAGE_URL
                        img = Image.open(open(valid_url, "rb")).resize((50, 50))
                        if player[5] != None: # player image url
                            valid_url = f'{BASE_IMAGE_URL}{player[5]}'
                            img = Image.open(requests.get(valid_url, stream=True).raw).resize((80, 80))
                        icon = ImageTk.PhotoImage(img)
                        iconLabel = Label(playerFrame, anchor="w")
                        iconLabel.image = icon
                        iconLabel.configure(image = icon)
                        iconLabel.grid(sticky='ew', row = 0, column=0, padx=10, pady=10, rowspan=4)
                        playerRole = playerRoles.get(player[0], "Player")
                        Label(playerFrame, text=f"Role: {playerRole}", anchor="w").grid(row=0, column=1, padx=10, pady=10, sticky="w")
                        Label(playerFrame, text=f"Name: {player[1]}", anchor="w").grid(row=1, column=1, padx=10, pady=10, sticky="w")
                        Label(playerFrame, text=f"Gender: {player[2]}", anchor="w").grid(row=2, column=1, padx=10, pady=10, sticky="w")
                        Label(playerFrame, text=f"Batting Style: {player[3]}", anchor="w").grid(row=3, column=1, padx=10, pady=10, sticky="w")
                        Label(playerFrame, text=f"Bowling Style: {player[4]}", anchor="w").grid(row=4, column=1, padx=10, pady=10, sticky="w")
                        playerFrame.grid(row=pcidx, column=pidx, padx=10, pady=10, sticky="ew")
                sinTeamFrame.grid(row=ridx, column=0, padx=10, pady=10, sticky="news")

        else: 
            Label(teamFrame, text="Team detail not available.", foreground="gray").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        teamFrame.grid(row=3, column=0, padx=10, pady=10, sticky="news")
        
        ## best players
        bestplFrame = LabelFrame(mainFrame, text="Best Players", background=frameColor, width=windowWidth, font={"Arial", 25})
        i = data_con[4]
        if i != [] and i != None:
            btData, blData = numpy.array_split(i, math.ceil(len(i)/2))
            # batting best player
            btbpFrame = LabelFrame(bestplFrame, text="Batting", borderwidth=2, highlightthickness=3, background="white", labelanchor="n", font=("Arial", 20))
            for btsidx, btsData in enumerate(btData):
                btssFrame = Frame(btbpFrame, borderwidth=2, highlightthickness=3, background="#e3ced5")
                valid_url = NO_IMAGE_URL
                img = Image.open(open(valid_url, "rb")).resize((50, 50))
                if btsData[11] != None:
                    valid_url = f'{BASE_IMAGE_URL}{btsData[11]}'
                    img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))

                icon = ImageTk.PhotoImage(img)

                iconLabel = Label(btssFrame)
                iconLabel.image = icon
                iconLabel.configure(image = icon, text=f"{btsData[7]} ({btsData[8]})", font={"Arial", 15}, anchor="w", background="#431d3c", foreground="white", compound="left")
                iconLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                    
                Label(btssFrame, text=f"Runs: {btsData[0]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                Label(btssFrame, text=f"Balls: {btsData[1]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=1, padx=10, pady=10, sticky="ew")
                Label(btssFrame, text=f"Fours: {btsData[2]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=2, padx=10, pady=10, sticky="ew")
                Label(btssFrame, text=f"Sixes: {btsData[3]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=0, padx=10, pady=10, sticky="ew")
                Label(btssFrame, text=f"Strike Rate: {btsData[6]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=1, padx=10, pady=10, sticky="ew")
                Label(btssFrame, text=f"Batting: {btsData[9]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=2, padx=10, pady=10, sticky="ew")

                if btsData[5] != None and btsData[5] != []:
                    valid_url = f'{BASE_IMAGE_URL}{btsData[11]}'
                    buf = btsData[5]
                    if buf != None:
                        img = Image.open(genWagonWheel(buf)).resize((500, 500))
                        icon = ImageTk.PhotoImage(img)
                        iconLabel = Label(btssFrame)
                        iconLabel.image = icon
                        iconLabel.configure(image = icon, anchor="w", background="#431d3c")
                        iconLabel.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=3, rowspan=3)

                btssFrame.grid(row=0, column=btsidx, padx=10, pady=10, sticky="news")
            btbpFrame.grid(row=0, column=0, padx=10, pady=10, sticky="news")

            # bowling best player
            blbpFrame = LabelFrame(bestplFrame, text="Bowling", borderwidth=2, highlightthickness=3, background="white", labelanchor="n", font=("Arial", 20))
            for blsidx, blsData in enumerate(blData):
                blssFrame = Frame(blbpFrame, borderwidth=2, highlightthickness=3, background="#e3ced5")
                valid_url = NO_IMAGE_URL
                img = Image.open(open(valid_url, "rb")).resize((50, 50))
                if blsData[10] != None:
                    valid_url = f'{BASE_IMAGE_URL}{blsData[10]}'
                    img = Image.open(requests.get(valid_url, stream=True).raw).resize((50, 50))

                icon = ImageTk.PhotoImage(img)

                iconLabel = Label(blssFrame)
                iconLabel.image = icon
                iconLabel.configure(image = icon, text=f"{blsData[6]} ({blsData[7]})", font={"Arial", 15}, anchor="w", background="#431d3c", foreground="white", compound="left")
                iconLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

                Label(blssFrame, text=f"Wickets: {blsData[0]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                Label(blssFrame, text=f"Balls: {blsData[1]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=1, padx=10, pady=10, sticky="ew")
                Label(blssFrame, text=f"Runs: {blsData[2]}", anchor="w", background="#059ea1")\
                    .grid(row=1, column=2, padx=10, pady=10, sticky="ew")
                Label(blssFrame, text=f"Economy: {blsData[5]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=0, padx=10, pady=10, sticky="ew")
                Label(blssFrame, text=f"Batting: {blsData[8]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=1, padx=10, pady=10, sticky="ew")
                Label(blssFrame, text=f"Bowling: {blsData[9]}", anchor="w", background="#059ea1")\
                    .grid(row=2, column=2, padx=10, pady=10, sticky="ew")

                blssFrame.grid(row=0, column=blsidx, padx=10, pady=10, sticky="news")
            blbpFrame.grid(row=1, column=0, padx=10, pady=10, sticky="news")
               
        else: 
            Label(bestplFrame, text="Best Players detail not available.", foreground="gray").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        bestplFrame.grid(row=4, column=0, padx=10, pady=10, sticky="news")
        
        mainFrame.grid(row=1, column=0, sticky="news")

    ## to do
    def embed_scorecard(self, mainFrame, data_con):
        self.clearFrame(mainFrame)
        mainFrame = DoubleScrolledFrame(mainFrame, type_=1, borderwidth=2, background="gray", height=410, width=windowWidth)
        return mainFrame

    ## to do
    def embed_commentary(self, mainFrame, data_con):
        self.clearFrame(mainFrame)
        mainFrame = DoubleScrolledFrame(mainFrame, type_=1, borderwidth=2, background="gray", height=410, width=windowWidth)
        return mainFrame
