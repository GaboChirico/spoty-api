from fastapi import FastAPI
from spoty import get_album_data, get_playlist_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/playlist/{playlist_id}")
async def get_playlist_info(playlist_id: str):
    return {"data": get_playlist_data(playlist_id)}

@app.get("/playlist/tracks/{playlist_id}")
async def get_playlist_tracks(playlist_id: str):
    return {"data": get_album_data(playlist_id)}
