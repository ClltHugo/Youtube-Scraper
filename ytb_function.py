from bs4 import BeautifulSoup
import requests
import json
import re
import argparse

def fichier_input(file):
    with open(file, 'r') as f:
        data = json.load(f)
        return data['videos_id']


def fichier_output(file, liste_dic):
    with open(file, 'w') as f:
        json.dump(liste_dic, f, indent=4, ensure_ascii=False)


def link_reading(url):
    youtube_url = url
    response = requests.request("GET", youtube_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_title(data):
    title = data['videoDetails']['title']
    return title


def get_author(data):
    author = data['videoDetails']['author']
    return author


def get_desc(data):
    desc = data['videoDetails']['shortDescription']
    return desc


def get_videoid(data):
    vid = data['videoDetails']['videoId']
    return vid


def get_video_likes(data):
    videoPrimaryInfoRenderer = data['contents']['twoColumnWatchNextResults'][
        'results']['results']['contents'][0]['videoPrimaryInfoRenderer']
    likes_str = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer'][
        'likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
    likes = likes_str.split(' ')[0].replace(',', '').split('\xa0')[0]
    likes_str = likes_str.split(' ')[0].replace(',', '')[:-6]
    likes_str = likes_str.replace('\u202f','')
    return(int(likes_str))


def dic_add(dic_video, data_info_base, data_likes):
    dic_video["titre_vid"] = get_title(data_info_base)
    dic_video["auteur_vid"] = get_author(data_info_base)
    dic_video["description_vid"] = get_desc(data_info_base)
    dic_video["id_vid"] = get_videoid(data_info_base)
    dic_video["description_urls"] = re.findall(
        r'(https?://\S+)', dic_video["description_vid"])
    dic_video["likes_vid"] = get_video_likes(data_likes)
    return dic_video


def all_infos(url):
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
