import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from ytb_function import *


#read the first line of the input.json
with open('input.json', 'r') as f:
    data = json.load(f)
    data = data['videos_id'][0]
    
url = "https://www.youtube.com/watch?v=" + data

dic_info_vid_un = all_infos(url)

#test du titre de la vidéo
def test_title():
    assert dic_info_vid_un["titre_vid"] == 'Hello kitty compilation Nouveaux épisodes - complet en francais'

#test de l'auteur de la vidéo
def test_author():
    assert dic_info_vid_un["auteur_vid"] == 'Chaine vince'
    
#test de la description de la vidéo
def test_desc():
    assert dic_info_vid_un["description_vid"] == "episode,dessin,complet,entier,cartoon,film,enfant,jeunesse,divertissment,"
    
#test de l'id de la vidéo
def test_id():
    assert dic_info_vid_un["id_vid"] == 'kzPpFoyMcXY'
    
#test le nombre de like > 0
def test_like():
    assert dic_info_vid_un["likes_vid"] >= 0
    
#test que la fonction input lit bien le fichier input.json
def test_input():
    assert fichier_input('input.json') != None

#test que la fonction link_reading renvoie bien le code
def test_link_reading():
    assert link_reading(url) != None
