# Movie Poster & Overview Downloader

A Python script that scans a folder containing movie directories, cleans up movie names, downloads high-quality posters, and saves movie overviews from The Movie Database (TMDb).

## Features
- **Cleans movie folder names** by removing extra text (e.g., resolutions, rip sources, release groups, actors, etc.).
- **Fetches high-quality posters** using the TMDb API and saves them in the corresponding movie folder.
- **Downloads movie overviews** and saves them as `info.txt` in each movie folder.
- **Progress tracking** with `tqdm`.

## Requirements
- Python 3.x
- TMDb API key (get one from [TMDb](https://www.themoviedb.org/))

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/movie-info-downloader.git
   cd movie-info-downloader
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
   python movie_info_downloader.py
   ```
3. Posters and overviews will be saved in each movie’s respective folder as `poster.jpg` and `info.txt`.

## Movie Name Cleaning
This script removes unnecessary details from folder names, including:
✅ **Dots replaced with spaces** → `The.Matrix.1999` → `The Matrix`
✅ **Years** → `(2004)`, `(1957)`, `-2019`, etc.
✅ **Resolutions & Quality Tags** → `1080p`, `720p`, `4K`, `HDR`, `WEB-DL`, `BluRay`, `DVDRip`, etc.
✅ **Release Groups & Torrent Tags** → `YTS`, `RARBG`, `GalaxyRG`, `anoXmous`, `PSA`, etc.
✅ **Bitrate & Encoding Info** → `x264`, `x265`, `H.264`, `10bit`, `6CH`, `DTS`, etc.
✅ **Director & Actor Names** → `Jean-Luc Godard`, `Andrei Tarkovsky`, etc.
✅ **File Size & FPS Details** → `1600MB`, `24fps`, `817kbs`, etc.

Example Cleanup:
```python
clean_movie_title("The.Matrix.1999.1080p.BluRay.x264")
# Output: "The Matrix"
```

