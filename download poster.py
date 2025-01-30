import os
import re
import requests
from tqdm import tqdm

# Replace with your actual TMDb API Key
TMDB_API_KEY = "e2757597236da6dca7f3dcfc613e7631"

# Base URL for poster images (w500 gives good quality)
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Path to the HDD folder containing movie folders
MOVIES_DIRECTORY = r"D:\Movies"  # Change this to your actual path

# Function to clean movie folder names (removes years, resolutions, extra text)
def clean_movie_title(folder_name):
    # Remove years (e.g., (2010), [1999], .2009, -2014, (Jean-Luc Godard, 1962))
    title = re.sub(r'[\(\[\.-]?(19|20)\d{2}[\)\]\.-]?', '', folder_name)
    
    # Remove director names & actors (e.g., "Jean-Luc Godard, 1962", "Andrei Tarkovsky")
    title = re.sub(r'\b(Jean-Luc Godard|Andrei Tarkovsky|Audrey Hepburn|Martin Scorsese|Quentin Tarantino|Christopher Nolan)\b', '', title, flags=re.IGNORECASE)

    # Remove resolutions, quality tags, bitrates, fps, and encoding details
    title = re.sub(r'\b(480p|720p|1080p|2160p|4K|HDR|WEB-DL|WEBRip|BluRay|BRRip|HDRip|DVDRip|HDTV|AMZN|XviD|x264|x265|HEVC|H\.?264|H\.?265|10bit|6CH|PSA|mSD|fps|kbs|abr)\b', '', title, flags=re.IGNORECASE)

    # Remove release groups & rip sources
    title = re.sub(r'\b(YTS|YIFY|RARBG|GalaxyRG|CM|IMAX|Proper|Unrated|Extended|HDB|anoXmous|WunSeeDee|MultiSub|Ultimate|Remastered|Special Edition)\b', '', title, flags=re.IGNORECASE)

    # Remove file size details (e.g., 1600MB)
    title = re.sub(r'\b\d{3,4}MB\b', '', title, flags=re.IGNORECASE)

    # Remove extra numbers (e.g., "12x304", "25fps", "817kbs")
    title = re.sub(r'\b\d+x\d+\b', '', title)

    # Remove bracketed terms: [YTS.MX], (1957), {BluRay}, [720p], etc.
    title = re.sub(r'[\[\(\{][^\]\)\}]*[\]\)\}]', '', title)

    # Remove extra symbols, dots, dashes, and multiple spaces
    title = re.sub(r'[\.\-_]', ' ', title)  # Replace dots, dashes, underscores with spaces
    title = re.sub(r'\s+', ' ', title).strip()  # Remove extra spaces

    return title

# Function to get movie poster URL from TMDb
def get_movie_poster(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return IMAGE_BASE_URL + poster_path
    return None

# Function to download and save the poster
def download_poster(movie_name, folder_path):
    poster_url = get_movie_poster(movie_name)
    
    if not poster_url:
        print(f"[❌] No poster found for: {movie_name}")
        return

    poster_path = os.path.join(folder_path, "poster.jpg")
    
    response = requests.get(poster_url, stream=True)
    if response.status_code == 200:
        with open(poster_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"[✅] Poster saved: {poster_path}")
    else:
        print(f"[❌] Failed to download: {movie_name}")

# Iterate through movie folders and fetch posters
def process_movie_folders():
    if not os.path.exists(MOVIES_DIRECTORY):
        print("Movies directory does not exist.")
        return
    
    movie_folders = [f for f in os.listdir(MOVIES_DIRECTORY) if os.path.isdir(os.path.join(MOVIES_DIRECTORY, f))]

    if not movie_folders:
        print("No movie folders found.")
        return

    print(f"Found {len(movie_folders)} movies. Downloading posters...\n")
    
    for movie in tqdm(movie_folders, desc="Downloading Posters"):
        cleaned_title = clean_movie_title(movie)  # Clean folder name before searching
        movie_folder_path = os.path.join(MOVIES_DIRECTORY, movie)
        download_poster(cleaned_title, movie_folder_path)

if __name__ == "__main__":
    process_movie_folders()
