from bs4 import BeautifulSoup
import requests
import json
import re
import argparse




"""
    This function is used to open a json file and return a list of video id
"""
def fichier_input(file: str) -> list:
    with open(file, 'r') as f:
        data = json.load(f)
        return data['videos_id']


"""
    This function is used to open the output json file
"""
def fichier_output(file , liste_dic: list) -> None:
    with open(file, 'w') as f:
        json.dump(liste_dic, f, indent=4, ensure_ascii=False)


"""
    Function that read the link and return a beautifulsoup object with all the informations
"""
def link_reading(url: str) -> BeautifulSoup:
    youtube_url = url
    response = requests.request("GET", youtube_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


"""
    Function that return the title of the video
"""
def get_title(data: dict) -> str:
    title = data['videoDetails']['title']
    return title


"""
    Function that return the author of the video
"""
def get_author(data: dict) -> str:
    author = data['videoDetails']['author']
    return author


"""
    Function that return the description of the video
"""
def get_desc(data : dict) -> str:
    desc = data['videoDetails']['shortDescription']
    return desc


"""
    Function that return the id of the video
"""
def get_videoid(data : dict) -> str:
    vid = data['videoDetails']['videoId']
    return vid


"""
    Function that return the number of likes of the video
"""
def get_video_likes(data : dict) -> int:
    videoPrimaryInfoRenderer = data['contents']['twoColumnWatchNextResults'][
        'results']['results']['contents'][0]['videoPrimaryInfoRenderer']
    likes_str = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer'][
        'likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
    likes = likes_str.split(' ')[0].replace(',', '').split('\xa0')[0]
    likes_str = likes_str.split(' ')[0].replace(',', '')[:-6]
    likes_str = likes_str.replace('\u202f','')
    return(int(likes_str))


"""
    Function that return a dictionary with all the informations of the video
"""
def dic_add(dic_video : dict, data_info_base : dict, data_likes : dict):
    dic_video["titre_vid"] = get_title(data_info_base)
    dic_video["auteur_vid"] = get_author(data_info_base)
    dic_video["description_vid"] = get_desc(data_info_base)
    dic_video["id_vid"] = get_videoid(data_info_base)
    dic_video["description_urls"] = re.findall(
        r'(https?://\S+)', dic_video["description_vid"])
    dic_video["likes_vid"] = get_video_likes(data_likes)
    return dic_video


"""
    Function that return all the informations of a video (used for the test)
"""
def all_infos(url : str) -> dict:
    dic_video = {}
    soup = link_reading(url)
    #First part data
    data_info_base = re.search(
        r"var ytInitialPlayerResponse = ({.*?});", soup.prettify()).group(1)
    data_info_base = json.loads(data_info_base)

    #Second part data (like)
    data_likes = re.search(
        r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_likes = json.loads(data_likes)
    dic_video = dic_add(dic_video, data_info_base, data_likes)
    return dic_video
