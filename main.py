###########################################################
#*                  GROUP 6 : main.py                    *#
#*                                                       *#
#*    Mark MONTHIEUX - Hugo DUJARDIN - Mathis FRANCOIS   *#
###########################################################

import pandas as pd
import recommendation
import streamlit as st

from recommendation import RecommendationEngine

re = RecommendationEngine()


lsr = pd.read_csv('./data/user_artists_gp6.dat', delimiter='\t').sort_values('userID')
lsr = lsr['userID'].to_list()

st.set_page_config(page_title="Recom Engine", page_icon=":balloon:", layout="wide", initial_sidebar_state="auto", menu_items=None)
with st.container(border=True):
    userid = st.number_input("Wich user ID you want to predict ?", value=2, step=1)
if userid:
    reco = re.get_recommandation(userid)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader(reco["first_music"][0], divider='rainbow')
        st.link_button("Go to website", url=reco["link_music"][0])
        st.image("https://www.marathon-bressedombes.fr/wp-content/uploads/2015/04/picto-musique.png")
        st.divider()
        st.caption(reco["name"][0])
        st.link_button("Check artist page", url=reco["url"][0])

    with col2:
        st.subheader(reco["first_music"][1], divider='rainbow')
        st.link_button("Go to website", url=reco["link_music"][1])
        st.image("https://i0.wp.com/vicken.fr/wp-content/uploads/2020/06/logo-musique-png-3.png")
        st.divider()
        st.caption(reco["name"][1])
        st.link_button("Check artist page", url=reco["url"][1])

    with col3:
        st.subheader(reco["first_music"][2], divider='rainbow')
        st.link_button("Go to website", url=reco["link_music"][2])
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Circle-icons-music.svg/2048px-Circle-icons-music.svg.png")
        st.divider()
        st.caption(reco["name"][2])
        st.link_button("Check artist page", url=reco["url"][2])
    
    with col4:
        st.subheader(reco["first_music"][3], divider='rainbow')
        st.link_button("Go to website", url=reco["link_music"][3])
        st.image("https://icons.iconarchive.com/icons/dtafalonso/yosemite-flat/512/Music-icon.png")
        st.divider()
        st.caption(reco["name"][3])
        st.link_button("Check artist page", url=reco["url"][3])
    
    with col5:
        st.subheader(reco["first_music"][4], divider='rainbow')
        st.link_button("Go to website", url=reco["link_music"][4])
        st.image("https://cdn.icon-icons.com/icons2/1880/PNG/512/iconfinder-music-4341309_120542.png")
        st.divider()
        st.caption(reco["name"][4])
        st.link_button("Check artist page", url=reco["url"][4])


