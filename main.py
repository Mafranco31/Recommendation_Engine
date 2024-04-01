###########################################################
#*                  GROUP 6 : main.py                    *#
#*                                                       *#
#*    Mark MONTHIEUX - Hugo DUJARDIN - Mathis FRANCOIS   *#
###########################################################

import pandas as pd
import recommendation

from recommendation import RecommendationEngine

re = RecommendationEngine()


lsr = pd.read_csv('./data/user_artists_gp6.dat', delimiter='\t').sort_values('userID')
lsr = lsr['userID'].to_list()
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width
for i in range(2, 3):
    userid = i

    if int(userid) in lsr:
        reco = re.get_recommandation(userid)
        print(reco)

    else:
        print("userID", userid, "not in database")
