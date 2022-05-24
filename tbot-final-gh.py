#Pip Requirements:
# boto3
# tweepy
# discord-webhook
from time import sleep
import tweepy
import boto3
from botocore.client import Config
import os
import sys 
from discord_webhook import DiscordWebhook

##Authenticating with Twitter

##Twitter access tokens
api_key = "YOUR_API_KEY"
api_secrets = "YOUR_API_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_secret = "YOUR_SECRET"

##Details needed to auth to twitter
auth = tweepy.OAuth1UserHandler(api_key,api_secrets,access_token,access_secret)

##Testing twitter auth
api = tweepy.API(auth)


##Authenticating with Digital Ocean

ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"

# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client('s3',
                        region_name='fra1',
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_access_key_id= ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)

try:
    for i in range (1, 146810):
        image_path = "frames/out{i}.jpg".format(i=i)
        image = "out{i}.jpg".format(i=i)
        ##temp downloading images saved in our storage space
        client.download_file('dmimagestore',image,image_path)
        print ("File Downloaded")
        #Value that will be tweeted
        tweet = "🔪American Psycho frame by frame - this is frame:"
        ##Path to image that will be uploaded
        print("##uploading image")
        media = api.media_upload(image_path)
        full_tweet = "{tweet} {i}".format(tweet=tweet, i=i)
        print("#Sending Tweet")
        api.update_status(status=full_tweet, media_ids=[media.media_id])
        ##Deleting downloaded content
        os.remove(image_path)
        sleep(40)
except:
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/978385396205518999/lL-o2YGr9AQ-_Rw1ZIv_DJqJUH_e7RWn31oQFalxyVRlVzWOliEX6xOz6ej1kI1SCNah', content='An error has occured with twitter bot and it has stopped posting')
    response = webhook.execute()
    sys.exit(1)

##We have about 144507 frames so we are going to repeat the post to twitter this number of times