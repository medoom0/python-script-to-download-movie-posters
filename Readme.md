# Movie Poster Downloader

A Python script that scans a folder containing movie directories, cleans up movie names, and downloads high-quality posters for each movie from The Movie Database (TMDb).

## Features
- Automatically **cleans movie folder names** by removing extra text (e.g., resolutions, rip sources, release groups, actors, etc.).
- Fetches **high-quality posters** using TMDb API.
- Saves each poster in the corresponding movie folder.
- Progress tracking with **tqdm**.

## Requirements
- Python 3.x
- TMDb API key (get one from [TMDb](https://www.themoviedb.org/))

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/movie-poster-downloader.git
   cd movie-poster-downloader
   ```
2. Install required dependencies:
   ```sh
   pip install requests tqdm
   ```

## Usage
1. **Set up your TMDb API key** in the script:
   ```python
   TMDB_API_KEY = "your_api_key_here"
   ```
2. **Run the script**:
   ```sh
   python download_posters.py 
   ```
3. Posters will be saved in each movie’s respective folder.

## Movie Name Cleaning
This script removes unnecessary details from folder names, including:
✅ **Years** → `(2004)`, `(1957)`, `-2019`, etc.
✅ **Resolutions & Quality Tags** → `1080p`, `720p`, `4K`, `HDR`, `WEB-DL`, `BluRay`, `DVDRip`, etc.
✅ **Release Groups & Torrent Tags** → `YTS`, `RARBG`, `GalaxyRG`, `anoXmous`, `PSA`, etc.
✅ **Bitrate & Encoding Info** → `x264`, `x265`, `H.264`, `10bit`, `6CH`, `DTS`, etc.
✅ **Director & Actor Names** → `Jean-Luc Godard`, `Andrei Tarkovsky`, etc.
✅ **File Size & FPS Details** → `1600MB`, `24fps`, `817kbs`, etc.

Example Cleanup:
```python
clean_movie_title("Interstellar_2014_1080p.x264 [DVDRip]")
# Output: "Interstellar"
```

## Contributing
Feel free to submit pull requests or open issues if you find bugs or have feature suggestions!

## License
This project is licensed under the MIT License.

