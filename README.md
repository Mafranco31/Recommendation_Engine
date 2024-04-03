
# Recommendation_Engine

This project is part of the Tbs BIG DATA semester of M1.
The purpose is to create a program that takes an user over the data base user_artists_gp6
and return 5 songs he might enjoy.

# Enrich the data

We scraped, using R, webpage of each artists in artists_gp6 taking theire 5 music tags
(RnB, Classic, jazz ...), theire 3 similar artists and theire first song.
We put all of this in artists_type.

# How works the recommendation engine

The engine uses 3 main algorythms to get the 5 recommended songs :

## Similar artists :
  The algorithm gets the similar artists of top 5 listened artists for each users and
  return the occurence of similars artists.

## Common tags :
  The algorithm gets the tags of the favorite artists of the user and return
  the artists that has similar tags, with a similarity percentage as value.

## Same users :
  The algorithm compare each favorite tags of each users and get the ones that 
