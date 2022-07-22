
import numpy as np
import matplotlib.pyplot as plt
import hashlib

import pandas as pd
import collectWikipediaData

def hash(message):

    digest = hashlib.sha1(message.encode())
    return int(digest.hexdigest(),16)

#--------------------------#
# ***Collect County Data***
#collectWikipediaData.run()
# ***Collect County Data***
#--------------------------#

data = r"""cordinates.txt"""

with open(data, "r") as f:
    dictionary = eval(f.read())


count = 0

data = {}
for county,lst in dictionary.items():
    
    county = ", ".join(["-".join(
                i for i in c.split("_County") if i) 
                    for c in county.strip("/wiki/").split(",_")]
            )

    cordinates = lst[0]
    cordinates['latitude'] = int(cordinates['latitude'].split(" ")[0]) 
    cordinates['longitude'] = int(cordinates['longitude'].split(" ")[0])
    
    data[county] = cordinates
    data[county]["countyName"] = county.split(", ")[0]
    data[county]["state"] = county.split(", ")[1]

    data[county]["stateID"] = hash(data[county]["state"])


df = pd.DataFrame(data).T


def graph():

    ax = plt.subplot(111)

    x = df.longitude
    y = df.latitude
    colors = df.stateID

    ax.scatter(x, y, c=colors)

    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)

    ax.set_ylabel('latitude')
    ax.set_xlabel('longitude')
    ax.set_title('Map of Counties by State and Cordinates')
    
    plt.show()

graph()
