import requests
from bs4 import BeautifulSoup
import re
import os
import sys

headers = {
    'authority': 'cdn-eu.anidb.net',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'referer': 'https://anidb.net/search/anime/?adb.search=black^%^20clover^&do.search=1',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'adbuin=1597645580-yvyi',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'DNT': '1',
    'Origin': 'https://anidb.net',
    'pragma': 'no-cache',
}

episode_list = []
bad_char = [';', ':', '<', '>', '"', '?']

# Function to get the episode list


def get_episodes():

    myURL = input("Enter the URL of the anime from anidb.net: ")
    source = requests.get(myURL, headers=headers)
    plain_text = source.text
    soup = BeautifulSoup(plain_text, "html.parser")
    episodes = soup.find_all("td", {"class": "title name episode"})

    max_num = int(input("Enter Total Number of episodes to fetch: "))
    for i in range(max_num):
        ep_dict = {}
        episode = episodes[i].find("label", {"itemprop": "name"})
        ep_name = episode.text.strip()
        for k in bad_char:
            ep_name = ep_name.replace(k, ' ')
        ep_dict = {
            "title": ep_name,
            "number": i+1
        }
        episode_list.append(ep_dict)
    print("Episode List has been Created \n\n")

    # print(episode_list)

# Function to rename the files


def rename_episodes():
    path = input("Enter the path of the folder: ")
    os.chdir(path)

    # To find the total number of episodes for numbering
    total_File_No = len(os.listdir(path))
    fill = len(str(total_File_No))

    for count, file in enumerate(os.listdir()):
        file_ext = os.path.splitext(file)[1]
        file_no = episode_list[count]["number"]
        name = episode_list[count]["title"]
        file_new = "{} - {}{}".format(str(file_no).zfill(fill), name, file_ext)
        os.rename(file, file_new)

    print("Files have been Renamed")


get_episodes()
rename_episodes()
