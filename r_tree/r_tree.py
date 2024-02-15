import pandas as pd
import os
import sys
from rtree import index

script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
df = pd.read_csv(CSV_PATH)

#Κλάση του RTree, περιέχει τις απαιτούμενες συναρτήσεις που θα χρησιμοποιηθούν 
class RTree:
    def __init__(self):
        self.index3d = index.Index(properties=index.Property(dimension=3))
        self.dataList = []

    def __str__(self):
        return "R Tree"

    def insert(self, itemId, item, x, y, z):
        self.index3d.insert(itemId, (x, y, z, x, y, z))
        self.dataList.append(item)
        
    def search(self, qbbox):
        return list(self.index3d.intersection(qbbox))
    
def letter_normalization(letter):
    return ord(letter.upper()) - 65

def create_rtree():
    df = pd.read_csv(CSV_PATH)
    rtree = RTree()
    for i in range(len(df)):
        x = letter_normalization(df.iloc[i]['Surname'][0])
        y = df.iloc[i]['#Awards']
        z = df.iloc[i]['DBLP']
        data = (df.iloc[i]['Surname'], df.iloc[i]['#Awards'], df.iloc[i]['DBLP'], df.iloc[i]['Education'])
        rtree.insert(i, data, x, y, z)
    return rtree


def query_rtree(rtree, minLetter, maxLetter, minAwards, minDBLP, maxDBLP):
    minLetter = letter_normalization(minLetter)
    maxLetter = letter_normalization(maxLetter)
    qbbox = (minLetter, minAwards, minDBLP, maxLetter, sys.maxsize, maxDBLP)
    matchingIds = rtree.search(qbbox)
    queryResults = []
    for id in matchingIds:
        queryResults.append(rtree.dataList[id])
        queryResults.sort(key=lambda x: x[0])
    return queryResults


def query_rtree_by_range(rtree, Letter_range, minAwards, DBLP_range):
    minLetter = letter_normalization(Letter_range[0])
    maxLetter = letter_normalization(Letter_range[1])
    qbbox = (minLetter, minAwards, DBLP_range[0], maxLetter, sys.maxsize, DBLP_range[1])
    matchingIds = rtree.search(qbbox)
    queryResults = []
    for id in matchingIds:
        queryResults.append(rtree.dataList[id])
        queryResults.sort(key=lambda x: x[0])
    return queryResults
