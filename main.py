from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import tkinter as tk
from tkinter import messagebox

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")


    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No aritsts with this name found")
        return None
    return json_result[0]

def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_artist():
    artist_name = artist_entry.get()
    if artist_name.strip() == "":
        messagebox.showerror("Input Error", "Please enter an artist name")
        return

    token = get_token()
    artist = search_for_artists(token, artist_name)
    if artist is None:
        messagebox.showinfo("No Results", "No artists with this name found")
        return
    
    artist_id = artist["id"]
    songs = get_songs_by_artists(token, artist_id)

    results_text.delete(1.0, tk.END)  
    results_text.insert(tk.END, f"Top Tracks for artist: {artist["name"]}\n")
    for idx, song in enumerate(songs):
        results_text.insert(tk.END, f"{idx + 1}. {song['name']}\n")

root = tk.Tk()
root.title("Spotify Artist Top Tracks")

tk.Label(root, text="Enter Artist Name:").pack(pady=10)
artist_entry = tk.Entry(root, width=50)
artist_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_artist)
search_button.pack(pady=10)

results_text = tk.Text(root, height=15, width=50)
results_text.pack(pady=10)

root.mainloop()
