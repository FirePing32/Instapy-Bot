from instabot import Bot 
from newsapi import NewsApiClient
import urllib.request
import os

from apscheduler.schedulers.blocking import BlockingScheduler
  
bot = Bot() 
bot.login(username = "YOUR_USERNAME",  
          password = "YOUR_PASSWORD") 

sched = BlockingScheduler()
newsapi = NewsApiClient(api_key='YOUR_API_KEY_HERE')

@sched.scheduled_job('interval', minutes=60)
def post_photo():

    all_articles = newsapi.get_everything(q='tech', sort_by='publishedAt', sources="techcrunch,the-verge,engadget,hacker-news", language='en', page=1)
    data = all_articles['articles'][0]

    title = data['title']
    author = data['author']
    description = data['description']
    post_url = data['url']
    image_url = data['urlToImage']
    urllib.request.urlretrieve(image_url, 'image.jpg')

    post_caption = "'" + title + "'" + " by " + author + "." + "\n" + description + "\n" + post_url
    
    bot.upload_photo("image.jpg", 
                 caption =post_caption)

post_photo()

sched.start()
