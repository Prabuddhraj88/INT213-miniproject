from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as mp
import numpy as np
import io

BASE_IMAGE_URL = "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_80/lsci"
NO_IMAGE_URL = "./resources/noimg.png"

colors = ["#f76f72", "#808080", "#00afdb"]
playerRoles = {
    "P": "Player",
    "VC": "Vice Captain",
    "C": "Captain",
    "WK": "Wicket Keeper",
    "CWK": "Captain Wicket Keeper",
}
windowWidth = 1400
windowHeight = 650

def cleanHTML(data):
    return bs(data, 'html.parser').text

def genWagonWheel(data):
    perc_data = []
    if sum(data) == 0: return None
    for i in data:
        perc_data.append((i/sum(data))*100)
    
    y = np.array(perc_data)
    mylabels = data

    mp.pie(y, labels = mylabels)
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    mp.cla()
    return buf
