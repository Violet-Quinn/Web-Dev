import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

# User input
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split('-')[0]
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = f"https://www.billboard.com/charts/hot-100/{date}"
responses = requests.get(url=url, headers=header)

if responses.status_code != 200:
    print(f"Error: Unable to fetch data. Status Code: {responses.status_code}")
    exit()

# Scraping song data
soup = BeautifulSoup(responses.text, "html.parser")
song_name_spans = soup.select("div ul li ul li h3")
song_names = [song.getText().strip() for song in song_name_spans]

# Display results
if song_names:
    print("\nTop Songs from Billboard Hot 100 on", date)
    for idx, song in enumerate(song_names[:100], start=1):  # Display first 100 songs
        print(f"{idx}. {song}")
else:
    print("No songs found. The website structure might have changed.")

# Spotify authentication setup
YOUR_APP_CLIENT_ID = "94002c240a8c425aab776eeb847fe35b"
YOUR_APP_CLIENT_SECRET = "0970b8f6905e474b84b45274707d1cc0"
YOUR_APP_REDIRECT_URI = "https://example.com"

sp_oauth = SpotifyOAuth(client_id=YOUR_APP_CLIENT_ID,
                         client_secret=YOUR_APP_CLIENT_SECRET,
                         redirect_uri=YOUR_APP_REDIRECT_URI,
                         scope="playlist-modify-private",
                        cache_path="token.txt")

# Get authorization URL
auth_url = sp_oauth.get_authorize_url()
print("Go to this URL for authentication:", auth_url)

# Prompt the user to authenticate and paste the redirected URL
response = input("Paste the full redirect URL here: ")

# Retrieve the access token
token_info = sp_oauth.get_access_token(response)
print("Token Info:", token_info)

# Use the token to interact with Spotify API
sp = spotipy.Spotify(auth=token_info['access_token'])

# Now you can proceed to interact with the Spotify API
user_id = sp.current_user()["id"]
print(f"Authenticated as: {user_id}")


track_uris = []
for song in song_names:
    try:
        # Search for the song with the track name and year
        query = f"track:{song} year:{year}"
        result = sp.search(q=query, type="track", limit=1)

        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
            print(f"Found: {song} - URI: {track_uri}")
        else:
            print(f"Song not found on Spotify: {song}")
    except Exception as e:
        print(f"Error searching for song '{song}': {e}")
        continue  # Skip to next song in case of an error

# Step 1: Create a New Private Playlist
playlist_name = f"{date} Billboard 100"
playlist_description = f"Top 100 songs from the Billboard Hot 100 on {date}"
playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_description)
playlist_id = playlist['id']

# Print the playlist ID
print(f"New playlist created with ID: {playlist_id}")

# Step 2: Add Songs to the Playlist
if track_uris:
    sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)
    print(f"\n{len(track_uris)} songs added to the playlist: {playlist_name}")
else:
    print("No songs to add to the playlist.")