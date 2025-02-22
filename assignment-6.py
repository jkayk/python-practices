# BLUEPRINT | DONT EDIT

import requests

movie_ids = [
    238, 680, 550, 185, 641, 515042, 152532, 120467, 872585, 906126, 840430
]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:

for movie_id in movie_ids:
    api_url = f"https://nomad-movies.nomadcoders.workers.dev/movies/{movie_id}"
    response = requests.get(api_url)
    data = response.json()
    title = data["title"]
    overview = data["overview"]
    vote_average = data["vote_average"]
    print(f"Title: {title}\nOverview: {overview}\nVote average: {vote_average}")