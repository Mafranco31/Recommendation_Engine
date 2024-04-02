###########################################################
#*             GROUP 6 : recommendation.py               *#
#*                                                       *#
#*    Mark MONTHIEUX - Hugo DUJARDIN - Mathis FRANCOIS   *#
###########################################################

import pandas as pd

class RecommendationEngine():
    '''
    Recommendation Engine gives us the function to get the recommanded artists to listen by giving a user id
    '''
    def __init__(self):
        '''initialize the class with the data'''
        # This part of the code is actived when we do re = RedommendationEngine()
        self.artists_type = pd.read_csv('./data/artists_type.csv', delimiter=';', index_col=0)
        self.artists_webinf = pd.read_csv('./data/artists_gp6.dat', delimiter='\t')
        self.user = pd.read_csv('./data/user_artists_gp6.dat', delimiter='\t').sort_values('userID')
        self.lsr = self.user['userID'].to_list()
        self.user_tags = pd.read_csv('./data/tags_by_usr.csv', delimiter=',')
        self.user_tags['tags'] = self.user_tags['tags'].apply(lambda x: eval(x))

    def get_similar_artists(self, userid, min_occurence=2, top=5):
        '''
        This function takes an user id and return the artists that are similar
        to the one that the user listen to. 

        Arg:
            arg1: id of the user
            arg2: minimum occurence to be accepted as a similar artist
            arg3: the number of top listened artists by the user we take to get the tag
        
        Return:
            the Serie of similar artists and their occurence
        '''

        # We sort the listened artists by the user by weight and extract the artists_id of the top 'top' artists
        v_artists_listened = self.user[self.user['userID'] == int(userid)].sort_values('weight', ascending=False)['artistID'].head(top).to_list()   
        
        # We extract from the database 'artists_type' the artists we have taken just before
        artists_id = pd.DataFrame(self.artists_type[self.artists_type['artist_id'].isin(v_artists_listened)])

        # We put the id's of the columns 'similar_artists1/2/3' of each artists_id in a pandas Series using .flatten() that flat to a list all values
        tag_id = pd.Series(artists_id.iloc[:, 2:5].values.flatten())

        # We drop the id : 0
        tag_id = tag_id[tag_id != 0]

        # We get the occurence of the id's
        tag_id = tag_id.value_counts()

        # We return the tags and theire occurence if they occure at least 'min_occurence' times
        tag_id = tag_id[tag_id >= min_occurence][:5]
        return tag_id
    

    def get_artists_by_tag(self, userid, mode='all', top=5, ret_nb=5, nb_top_artists=15000):
        """
        This function get the artists that the user doesn't listen
        but with tags that match

        Arg:
            arg1: Dictionary of tags of the user
            arg2: id of the user
            arg3: the number of top artists we take as example for the user to get his tags
            arg4: return number of artists
            arg5: the number of artists we take by sorting by weight of listen
        
        Return:
            the Serie of similar artists by tags
        """
        # We sort the listened artists by the user by weight and extract the artists_id of the top 'top' artists 
        v_artists_listened_top = self.user[self.user['userID'] == int(userid)].sort_values('weight', ascending=False)['artistID'].head(top).to_list()   
        
        # We extract from the database 'artists_type' the artists we have taken just before and drop all the columns except the music tags.
        artists_id = pd.DataFrame(self.artists_type[self.artists_type['artist_id'].isin(v_artists_listened_top)].drop(['first_music', 'similar_artists1', 'similar_artists2', 'similar_artists3'], axis=1))

        # We put the tags of the columns 'music_tag1/2/3/4/5' of each artists_id in a pandas Series using .flatten() that flat to a list all values
        tags = pd.Series(artists_id.iloc[:, 1:].values.flatten())

        # We use the function value_counts to count the occurence of values of the serie 'tags'
        d_tags = tags.value_counts()

        # We get the sum of the top 5 of tags of the user to have the maximum potential score an artist can have
        sum_tags = sum(d_tags[:5])

        # We sort by weight artists and get the first 'nb_top_artists' artists
        artists_weight = self.user.groupby('artistID').sum().drop('userID', axis=1).sort_values('weight', ascending=False).head(nb_top_artists).index

        # We extract from artists_type the artists that are in artists_weight created just before
        top_artists = pd.DataFrame(self.artists_type[self.artists_type['artist_id'].isin(artists_weight)].set_index('artist_id'))

        if mode == 'all':
            # We extract all the artists of top_artists that have all theire tags matching with user's tags
            artists_with_tags = top_artists[top_artists.iloc[:, 5:].isin(d_tags.index.tolist()).all(axis=1)]
        else:
            # We extract all the artists of top_artists that have at least 1 tag matching with user's tags
            artists_with_tags = top_artists[top_artists.iloc[:, 5:].isin(d_tags.index.tolist()).any(axis=1)]

        # We sort the listened artists by the user by weight and extract the artists_id
        v_artists_listened = self.user[self.user['userID'] == int(userid)]['artistID'].to_list()

        # We drop all the artists that are already listened by the user (using ~ .isin() that is the contrary of .isin()) and we drop the columns that we are not interested about
        artists_with_tags = artists_with_tags[~artists_with_tags.index.isin(v_artists_listened)].drop(['first_music', 'similar_artists1', 'similar_artists2', 'similar_artists3'], axis=1)

        # We create a new column 'score' that is the sum of the value of tags in d_tags for each rows (artists)
        artists_with_tags['score'] = artists_with_tags.apply(lambda row: sum([d_tags.get(row[tag], 0) for tag in ['music_tag1', 'music_tag2', 'music_tag3', 'music_tag4', 'music_tag5']]), axis=1)
        
        # We create a new column 'score_percent' that is the percentage of the maximum score possible each rows (artists) have by theire score
        artists_with_tags['score_percent'] = round(artists_with_tags['score'] / sum_tags * 100, 0)

        # We sort the results by score
        artists_with_tags = artists_with_tags.sort_values('score', ascending=False)

        # We create a dataframe with 'artist_id', 'score', and 'score_percent' and we keep only the first 'ret_nb' of artists
        v_reco = pd.DataFrame(artists_with_tags.drop(['score', 'music_tag1', 'music_tag2', 'music_tag3', 'music_tag4', 'music_tag5'], axis=1).head(ret_nb))

        # We return the dataframe as a dictionary
        return v_reco['score_percent']

    def _get_abs_dif_tags(self, new_tag, tag):
        '''
        This function is used in find_similar_user to get the absolute
        sum of difference between tags
        '''
        tot = 0
        for i in tag:
            if i in new_tag:
                tot += abs(new_tag[i] - tag[i])
        if tot >= 100:
            return 100
        return 100 - tot

    def find_similar_user(self, userid):
        '''
        This function gets the top listened artists by users that have same
        tags than the user

        Arg:
            arg1: The userid
        
        Return:
            the list of the top listened artists by similar users and thiere
            occurence
        '''
        # We get the tag of the userid
        tag = self.user_tags[self.user_tags['userID'] == userid]['tags'].iloc[0]
        l_same_usr = {}
        equal = 5
        # We iterate over the list of the data 'user_tags' to find users that have the same top of tags
        while (equal > 2 and len(l_same_usr) < 30):
            for i in range(len(self.user_tags)):
                if sum(1 for x, y in zip(list(self.user_tags['tags'][i].keys())[:equal], list(tag.keys())[:equal]) if x == y) == equal and self.user_tags['userID'][i] != userid:
                    dif = {}
                    # If we found one, we put its index in 'l_same_usr' and it's similarity value as value with the function '_get_abs_dif_tags'
                    l_same_usr[self.user_tags['userID'][i]] = self._get_abs_dif_tags(self.user_tags['tags'][i], tag)

                if (len(l_same_usr) >= 30):
                    break
            equal = equal - 1
        # If we dont have enought users, we repeat but without order the operation, and only for top 3
        if len(l_same_usr) < 30:
            for i in range(len(self.user_tags)):
                if sum(1 for x in list(self.user_tags['tags'][i].keys())[:4] for y in list(tag.keys())[:4] if x == y) == 3 and self.user_tags['userID'][i] != userid:
                    dif = {}
                    l_same_usr[self.user_tags['userID'][i]] = self._get_abs_dif_tags(self.user_tags['tags'][i], tag)
                if (len(l_same_usr) >= 30):
                    break

        # Then we create a dictionary sorting our similar users by theire value and keeping top 10
        d_same_usr = dict(sorted(l_same_usr.items(), key=lambda x:x[1], reverse = True)[:10])
        # In the top 10 we keep only keys that has value >= 80
        d_usr = {key: value for key, value in d_same_usr.items() if value >= 80}
        ret = []
        # We create a list of the top 10 listened artists of similar users
        for key in d_usr:
            ret.append(self.user[self.user['userID'] == key].sort_values('weight', ascending=False)['artistID'].head(10).to_list())
        flattened_list = [item for sublist in ret for item in sublist]

        # We remove artists that user listen to already
        v_artists_listened = self.user[self.user['userID'] == int(userid)]['artistID'].to_list()
        for x in flattened_list:
            if x in v_artists_listened:
                flattened_list.remove(x)

        # We return the dictionary of artists_id and theire occurence
        fl = pd.Series(flattened_list).value_counts()
        fl = fl[fl.values > 1][:5]
        return fl
    
    def _get_top200_final(self, userid, l_ret, exist=True):
        '''
        This function is used at the end if it miss recommendation.
        It get the top 200 and returns the number of reco the user needs

        Arguments:
            arg1: id of the user
            arg2: actual list of return
            arg3: boolean if the userid exists or not

        Return:
            list of artists recommended
        '''

        # We sort by weight artists and get the first 'nb_top_artists' artists
        artists_weight = self.user.groupby('artistID').sum().drop('userID', axis=1).sort_values('weight', ascending=False).head(200).index

        # We extract from artists_type the artists that are in artists_weight created just before
        top_artists = self.artists_type[self.artists_type['artist_id'].isin(artists_weight)]['artist_id'].tolist()

        if exist:
            v_artists_listened = self.user[self.user['userID'] == int(userid)]['artistID'].to_list()
            k = len(l_ret)
            for item in top_artists:
                if item not in l_ret and item not in v_artists_listened:
                    l_ret.append(item)
                    k += 1
                if k == 5:
                    break
        else:
            k = len(l_ret)
            for item in top_artists:
                if item not in l_ret:
                    l_ret.append(item)
                    k += 1
                if k == 5:
                    break
        return l_ret
            


    def get_recommandation(self, userid):
        '''
        This function is the main function of RecommendationEngine.
        It takes an userid and returns the computed top5 recommendation
        for this user.
        
        Arguments:
            arg1: id of the user
            
        Returns:
            The list of the songs he might enjoy
        '''
        
        l_ret = []

        l_art = self.artists_webinf['id'].tolist()
        # If the number of answers is not enought, we do get_artists_by_tags in 'any' mode, that means that
        # if will take all the artists of top '500' that has at least 1 tag that has the user
        if userid in self.lsr:
            # We do our 3 recommendation function
            sim = self.get_similar_artists(userid, 2, 10) 
            tags = self.get_artists_by_tag(userid)
            usr_sim = self.find_similar_user(userid)
            
            # We get the number of answers
            tot = len(sim) + len(tags) + len(usr_sim)
            if tot < 5:
                tags2 = {}
                tags2 = self.get_artists_by_tag(userid, mode='any', ret_nb = 10 - tot, nb_top_artists=500)
                tot += len(tags2)
                if tot < 5:
                    print("user :", userid, "has a total of :", tot)
                # Then we append all our results in the result list
                k = 0
                for art1 in range(len(sim)):
                    if sim.index[art1] not in l_ret and sim.index[art1] in l_art:
                        l_ret.append(sim.index[art1])
                        k += 1
                for art2 in range(len(tags)):
                    if tags.index[art2] not in l_ret and tags.index[art2] in l_art:
                        l_ret.append(tags.index[art2])
                        k += 1
                for art3 in range(len(usr_sim)):
                    if usr_sim.index[art3] not in l_ret and usr_sim.index[art3] in l_art:
                        l_ret.append(usr_sim.index[art3])
                        k += 1
                for art4 in range(len(tags2)):
                    if tags2.index[art4] not in l_ret and tags2.index[art4] in l_art:
                        l_ret.append(tags2.index[art4])
                        k += 1
                    if k == 5:
                        break
            else:
                # Otherwise we add the 3 first recommendation from get_artists_by_tag that we consider as more
                # relevant overall
                len_tags = len(tags)
                k = min(len_tags, 3)
                t = 0
                for t in range(k):
                    if tags.index[t] in l_art:
                        l_ret.append(tags.index[t])
                
                y = 0
                z = 0
                # Then we fill the rest with the higest values of get_similar_artists and find_similar_user
                while (len(l_ret) < 5 and not (len(sim) - y == 0 and len(usr_sim) - z == 0)):
                    if len(sim) - y == 0 and len(usr_sim) - z > 0:
                        if usr_sim.index[z] not in l_ret and usr_sim.index[z] in l_art:
                            l_ret.append(usr_sim.index[z])
                        z += 1
                    elif len(usr_sim) - z == 0 and len(sim) - y > 0:
                        if sim.index[y] not in l_ret and sim.index[y] in l_art:
                            l_ret.append(sim.index[y])
                        y += 1
                    elif len(usr_sim) - z > 0 and len(sim) - y > 0:
                        if sim.iloc[y] > usr_sim.iloc[z]:
                            if sim.index[y] not in l_ret and sim.index[y] in l_art:
                                l_ret.append(sim.index[y])
                            y += 1
                        else:
                            if usr_sim.index[z] not in l_ret and usr_sim.index[z] in l_art:
                                l_ret.append(usr_sim.index[z])
                            z += 1
                    k += 1
                # If we have not enough, we ask an other time to get_artists_by_tag list
                while (len(l_ret) < 5 and t < len(tags)):
                    if tags.index[t] not in l_ret and tags.index[t] in l_art:
                        l_ret.append(tags.index[t])
                    t += 1
            if len(l_ret) != 5:
                l_ret = self._get_top200_final(userid, l_ret)
    
        else:
            l_ret = self._get_top200_final(userid, l_ret, exist=False)

        # Then we use our return list to keep all values of artists_webinf that match
        l_ret_info = pd.DataFrame(self.artists_webinf[self.artists_webinf['id'].isin(l_ret)])
        
        # We do a left join with artist_webinf and the artists_type database to get the name of the first music of the artist
        l_ret_info = l_ret_info.rename(columns={'id':'artist_id'})
        column_selected = self.artists_type[['artist_id', 'first_music']]
        merged_ret = pd.merge(l_ret_info, column_selected, on='artist_id', how='left')

        # With the name of the music, we can create the url that leads to the music webpage and add it in our return table
        merged_ret['link_music'] = merged_ret.apply(lambda row: row['url'] + "/_/" + row['first_music'].replace(' ','+') if pd.notna(row['first_music']) else row['url'], axis=1)
        return merged_ret
