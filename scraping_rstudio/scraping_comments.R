###########################################################
#*            GROUP 6 : scrapping_comments.R             *#
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
artists_comment <- data.frame(artist_id = numeric(), stringsAsFactors = FALSE)

# Build the vector of website's url
v_url <- artists[3]
v_url

# For boucle that scrap webpage
for (i in 1:15000) {
  # Take the i's url
  url <- v_url[i, ]
  url <- paste0(url, "/+shoutbox?sort=popular")
  tryCatch({
    # Read webpage
    webpage <- read_html(url)
    
    # Extract up to 5 music tag type
    comment_html <- html_nodes(webpage, ".shout-body p")
    comment <- html_text(comment_html)[0:49]

    comment <- paste(comment, collapse = "\t")
    # Create a data frame for the current webpage
    artists_comment_temp <- data.frame(artist_id = artists$id[i],
                               comments = comment,
                               stringsAsFactors = FALSE)
    
    # Append the data frame to the main data frame
    artists_comment <- bind_rows(artists_comment, artists_comment_temp)
    
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
print(artists_comment)

# Create the artists_type.dat file
write.csv2(artists_comment,
           file = "/Users/mathis/Desktop/Tbs_BigData_Bcn/projet_final/data/artists_comments.csv",
           row.names = T)
