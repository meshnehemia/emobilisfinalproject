from django.shortcuts import render
from googleapiclient.discovery import build

# Create your views here.
API_KEY = 'AIzaSyCYi5viDwayCM4yCMuGSBQI2_W0HQlcU0U'
# API_KEY = 'AIzaSyCxYuPnvD8a7NqQdFYRmxGmJRH-uDqFav8'
youtube = build('youtube', 'v3', developerKey=API_KEY)


def home(request):
    context = arrange_youtube_data("python")
    return render(request, 'entertainment/index.html', context)


def data(query):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=20
    )

    return request.execute()


def arrange_youtube_data(query):
    response = data(query)
    video = []
    for item in response['items']:
        video.append({
            "url": f"https://www.youtube.com/embed/{item['id']['videoId']}",
            "title": item['snippet']['title'],
            "channel": item['snippet']['channelTitle'],
            "thumbnail": item['snippet']['thumbnails']['medium']['url'],
            "description": item['snippet']['description'],
            "published_at": item['snippet']['publishedAt']
        })
    context = {"response": video}
    return context


def get_youtube_data(request):
    query = request.GET['query']
    context = arrange_youtube_data(query)
    return render(request, 'entertainment/index.html', context)
