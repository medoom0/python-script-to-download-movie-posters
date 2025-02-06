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
    title = folder_name.replace(".", " ")  # Replace dots with spaces
    title = re.sub(r'[\(\[\.-]?(19|20)\d{2}[\)\]\.-]?', '', title)
    title = re.sub(r'\b(Jean-Luc Godard|Andrei Tarkovsky|Audrey Hepburn|Martin Scorsese|Quentin Tarantino|Christopher Nolan)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b(480p|720p|1080p|2160p|4K|HDR|WEB-DL|WEBRip|BluRay|BRRip|HDRip|DVDRip|HDTV|AMZN|XviD|x264|x265|HEVC|H\.?264|H\.?265|10bit|6CH|PSA|mSD|fps|kbs|abr)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b(YTS|YIFY|RARBG|GalaxyRG|CM|IMAX|Proper|Unrated|Extended|HDB|anoXmous|WunSeeDee|MultiSub|Ultimate|Remastered|Special Edition)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b\d{3,4}MB\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b\d+x\d+\b', '', title)
    title = re.sub(r'[\[\(\{][^\]\)\}]*[\]\)\}]', '', title)
    title = re.sub(r'[\._-]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

# Function to get movie details from TMDb
def get_movie_details(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]  # Return the first search result
    return None

# Function to save movie overview to info.txt
def save_overview(movie_name, folder_path):
    movie_details = get_movie_details(movie_name)
    overview = movie_details.get("overview", "No overview available.") if movie_details else "No overview available."
    info_path = os.path.join(folder_path, "info.txt")
    
    with open(info_path, "w", encoding="utf-8") as file:
        file.write(overview)
    
    print(f"[✅] Overview saved for '{movie_name}' in: {info_path}")

# Function to download and save the poster
def download_poster(movie_name, folder_path):
    movie_details = get_movie_details(movie_name)
    poster_path = movie_details.get("poster_path") if movie_details else None
    
    if not poster_path:
        print(f"[❌] No poster found for: {movie_name}")
        return
    
    poster_url = IMAGE_BASE_URL + poster_path
    poster_file_path = os.path.join(folder_path, "poster.jpg")
    
    response = requests.get(poster_url, stream=True)
    if response.status_code == 200:
        with open(poster_file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"[✅] Poster saved: {poster_file_path}")
    else:
        print(f"[❌] Failed to download: {movie_name}")

# Iterate through movie folders and fetch both posters and overviews
def process_movie_folders():
    if not os.path.exists(MOVIES_DIRECTORY):
        print("Movies directory does not exist.")
        return
    
    movie_folders = [f for f in os.listdir(MOVIES_DIRECTORY) if os.path.isdir(os.path.join(MOVIES_DIRECTORY, f))]
    
    if not movie_folders:
        print("No movie folders found.")
        return
    
    print(f"Found {len(movie_folders)} movies. Fetching details...\n")
    
    for movie in tqdm(movie_folders, desc="Processing Movies"):
        cleaned_title = clean_movie_title(movie)
        print(f"Processing: {cleaned_title}")  # Show movie being processed
        movie_folder_path = os.path.join(MOVIES_DIRECTORY, movie)
        save_overview(cleaned_title, movie_folder_path)
        download_poster(cleaned_title, movie_folder_path)

if __name__ == "__main__":
    process_movie_folders()
