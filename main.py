from ossapi import Ossapi
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')


api = Ossapi(client_id, client_secret)

falsia_id = 6693174


def get_rank(id):
    player = api.user(id)
    rank = player.statistics.global_rank
    return rank


#get beatmap_id, pp, mods
def get_top_scores(id):
    top50_scores = api.user_scores(id, mode ='osu', type='best', limit=50)

    scores = []


    for i in range(len(top50_scores)):
        beatmap_id = top50_scores[i].beatmap.id
        pp = top50_scores[i].pp
        mods = top50_scores[i].mods
        mods = str(mods)

        scores.append([beatmap_id, pp, mods])


    return scores



player_dict = {}


def main():

    # key: rank
    # value: top_scores

    for user_id in range(2, 15000000):
        try:
            #get player's rank
            rank = get_rank(user_id)


            #get player's top_scores
            scores = get_top_scores(user_id)

            #add into dictionary

            player_dict[rank] = scores

            print("player_id", user_id, "added")

        except:
            print("something went wrong" , user_id)


main()

print(player_dict)

df = pd.DataFrame(data = player_dict, columns=['BEATMAP_ID', 'PP_VALUE', 'MODS'])
df = (df.T)

df.to_excel('player_dict.xlsx')








