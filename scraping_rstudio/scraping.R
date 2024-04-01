###########################################################
#*                GROUP 6 : scrapping.R                  *#
#*                                                       *#
#*    Mark MONTHIEUX - Hugo DUJARDIN - Mathis FRANCOIS   *#
###########################################################


# Replace the path with your file's path
path_artists = "/Users/mathis/Desktop/Tbs_BigData_Bcn/projet_final/data/artists_gp6.dat"
path_user_artists = "/Users/mathis/Desktop/Tbs_BigData_Bcn/projet_final/data/user_artists_gp6.dat"

# Create database with artists file
artists = read.table(path_artists, sep= "\t", stringsAsFactors = F,
                     comment.char = "", quote = "", header = T)
str(artists)

# Create database with user_artists file
user_artists = read.table(path_user_artists, sep = "\t", header = T)
str(user_artists)

library('rvest')
library('dplyr')

v_url <- artists[3]

# Function that get the artist_id in artists database by its name
get_artists_id <- function(v) {
  v_id <- vector()
  for (i in 1:3) {
    if (v[i] %in% artists$name) {
      v_id <- c(v_id, artists$id[artists$name == v[i]])
    }
    else {
      v_id <- c(v_id, 0)
    }
  }
  return (v_id)
}

# Build the data base
artists_type <- data.frame(artist_id = numeric(), first_music = character(),
                           similar_artists1 = numeric(),
                           similar_artists2 = numeric(), 
                           similar_artists3 = numeric(),
                           music_tag1 = character(),  music_tag2 = character(),
                           music_tag3 = character(), music_tag4 = character(),
                           music_tag5 = character(), stringsAsFactors = FALSE)

# Build the vector of website's url
v_url <- artists[3]

# For boucle that scrap webpage
for (i in 1:15000) {
  # Take the i's url
  url <- v_url[i, ]
  tryCatch({
    # Read webpage
    webpage <- read_html(url)
    
    # Extract up to 5 music tag type
    music_tag_html <- html_nodes(webpage, ".tag a")
    music_tag <- html_text(music_tag_html)[0:5]
    
    # Extract up to 3 similar artists
    similar_artists_html <- html_nodes(webpage,
                                       ".artist-similar-artists-sidebar-item-name a")
    similar_artists_name <- html_text(similar_artists_html)[0:3]
    similar_artists <- get_artists_id(similar_artists_name)
    
    # Extract the top 1 song of the artist
    first_music_html <- html_nodes(webpage, ".chartlist-name a")
    first_music <- html_text(first_music_html)[0:1]  # Collect up to 1 values
    
    # Create a data frame for the current webpage
    artists_temp <- data.frame(artist_id = artists$id[i],
                               first_music = first_music[1][1],
                               similar_artists1 = similar_artists[1][1],
                               similar_artists2 = similar_artists[2][1],
                               similar_artists3 = similar_artists[3][1],
                               music_tag1 = music_tag[1][1],
                               music_tag2 = music_tag[2][1],
                               music_tag3 = music_tag[3][1],
                               music_tag4 = music_tag[4][1],
                               music_tag5 = music_tag[5][1],
                               stringsAsFactors = FALSE)
    
    # Append the data frame to the main data frame
    artists_type <- bind_rows(artists_type, artists_temp)
    
    # Print progress message
    cat("\033[1;32mProcessed webpage", i, "\n\033[0m")
  }, error = function(e) {
    #Print error message
    cat("\033[1;31mError occurred while processing webpage:", i, "\n\033[0m")
  })
  #To avoid overwhelming the server with requests
  #Sys.sleep(round(runif(1, min = 0.1, max = 0.3), digits = 2))
}
# Print the collected data
print(class(artists_type))

# Create the artists_type.dat file
write.csv2(artists_type,
           file = "/Users/mathis/Desktop/Tbs_BigData_Bcn/projet_final/data/artists_type.csv",
           row.names = T)
