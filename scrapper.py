from ytb_function import *



parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Input JSON file with URLs', required=True)
parser.add_argument('--output', help='Output JSON file with data', required=True)
args = parser.parse_args()
argdict = vars(args)
input_parameter = argdict['input']
output_parameter = argdict['output']
input_json = fichier_input(input_parameter)
    
#initialisation de la liste de dictionnaire
liste_dic =[]
#url dynamique avec format dans la boucle for
url_base = 'https://www.youtube.com/watch?v={video_id}'

#boucle for pour parcourir la liste des id des vidéos
for element in input_json:
        
    dic_video = {}
    url = url_base.format(video_id=element)
    
    try:
        #Reading de la page
        soup = link_reading(url)

        #First part data
        data_info_base = re.search(
            r"var ytInitialPlayerResponse = ({.*?});", soup.prettify()).group(1)
        data_info_base = json.loads(data_info_base)

        #Second part data (like)
        data_likes = re.search(
            r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
        data_likes = json.loads(data_likes)

        #add the information in the dictionary
        dic_video = dic_add(dic_video, data_info_base, data_likes)

        #Add the dictionary to the list
        liste_dic.append(dic_video)
    except:
        pass 
    
#write the list of dictionary in a json file
fichier_output(output_parameter,liste_dic)
