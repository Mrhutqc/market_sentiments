import datetime
from pytwitter import Api
import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from TwitterAPI import TwitterAPI


# api = Api(bearer_token=bearer_token)
# Compute The Negative, Neutral, Positive Analysis
def analysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


# Clean The Data
def cleantext(text):
    text = re.sub(r"@[A-Za-z0-9]+", "", text)  # Remove Mentions
    text = re.sub(r"#", "", text)  # Remove Hashtags Symbol
    text = re.sub(r"RT[\s]+", "", text)  # Remove Retweets
    text = re.sub(r"https?:\/\/\S+", "", text)  # Remove The Hyper Link

    return text


# Get The Subjectivity
def sentiment_analysis(ds):
    sentiment = TextBlob(ds["tweet"]).sentiment
    return pd.Series([sentiment.subjectivity, sentiment.polarity])


# elonmusk = api.get_user(username="elonmusk")
# charlesHoskinson = api.get_user(username="IOHK_Charles")
#
#
# # Max 100 tweets
# muskTweets = api.get_timelines(user_id=elonmusk.data.id, max_results=50)
# charlesHoskinsonTweets = api.get_timelines(user_id=elonmusk.data.id, max_results=50)
#
# dfMusk = pd.DataFrame([tweet.text for tweet in muskTweets.data], columns=["tweet"])
# dfCharles = pd.DataFrame([tweet.text for tweet in charlesHoskinsonTweets.data], columns=["tweet"])
#
# df = pd.concat([dfMusk, dfCharles])
#
# # Clean The Text
# df["tweet"] = df["tweet"].apply(cleantext)
#
# # Adding Subjectivity & Polarity
# df[["subjectivity", "polarity"]] = df.apply(sentiment_analysis, axis=1)
#
# allwords = " ".join([twts for twts in df["tweet"]])
# wordCloud = WordCloud(width=1000, height=1000, random_state=21, max_font_size=119).generate(allwords)
# plt.figure(figsize=(20, 20), dpi=80)
# plt.imshow(wordCloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()
#
# # Create a New Analysis Column
# df["analysis"] = df["polarity"].apply(analysis)
# # Print The Data
#
# positive_tweets = df[df['analysis'] == 'Positive']
# negative_tweets = df[df['analysis'] == 'Negative']
#
# plt.figure(figsize=(10, 8))
# for i in range(0, df.shape[0]):
#     plt.scatter(df["polarity"][i], df["subjectivity"][i], color="Red")
# plt.title("Sentiment Analysis") # Add The Graph Title
# plt.xlabel("Polarity") # Add The X-Label
# plt.ylabel("Subjectivity") # Add The Y-Label
# plt.show() # Showing The Graph
#
# print(len(positive_tweets) / len(negative_tweets))
#
# print("done")

# api = TwitterAPI(api_key, api_secret_key, access_token, access_token_secret, api_version='2')
# r = api.request('tweets/search/recent', {
#         'query':'bitcoin',
#         'tweet.fields':'author_id',
#         'expansions':'author_id'})
# for item in r:
#     print(item)

from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

QUERY = 'from:mrhutqc from:el_billy1'

try:
    o = TwitterOAuth.read_file()
    api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

    # GET STREAM RULES

    rule_ids = []
    r = api.request('tweets/search/stream/rules', method_override='GET')
    for item in r:
        if 'id' in item:
            rule_ids.append(item['id'])
        else:
            print(json.dumps(item, indent=2))

    # DELETE STREAM RULES

    if len(rule_ids) > 0:
        r = api.request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
        print(f'[{r.status_code}] RULES DELETED: {json.dumps(r.json(), indent=2)}\n')

except TwitterRequestError as e:
    print(e.status_code)
    for msg in iter(e):
        print(msg)

except TwitterConnectionError as e:
    print(e)

except Exception as e:
    print(e)

try:
    o = TwitterOAuth.read_file()
    api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

    QUERY = "from:elonmusk OR from:el_billy1 BTC OR from:Mrhutqc BTC"

    # ADD STREAM RULES
    r = api.request('tweets/search/stream/rules', {'add': [{'value': QUERY}]})

    # QUERY = "BTC OR bitcoin OR crypto"
    #
    # # ADD STREAM RULES
    # z = api.request('tweets/search/stream/rules', {'add': [{'value': QUERY}]})

    print(f'[{r.status_code}] RULE ADDED: {r.text}')
    if r.status_code != 201:
        exit()

    # GET STREAM RULES

    r = api.request('tweets/search/stream/rules', method_override='GET')
    print(f'[{r.status_code}] RULES: {r.text}')
    if r.status_code != 200:
        exit()

    # START STREAM

    r = api.request('tweets/search/stream')
    print(f'[{r.status_code}] START...')
    if r.status_code != 200:
        exit()
    for item in r:
        print(item)

except TwitterRequestError as e:
    print(e.status_code)
    for msg in iter(e):
        print(msg)

except TwitterConnectionError as e:
    print(e)

except Exception as e:
    print(e)
#
# from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
# import json
#
# QUERY = '"crypto" OR "bitcoin"'
# EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
# TWEET_FIELDS = 'author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'
# USER_FIELDS ='created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'
#
# try:
#     o = TwitterOAuth.read_file()
#     api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')
#
#     # ADD STREAM RULES
#
#     r = api.request('tweets/search/stream/rules', {'add': [{'value':QUERY}]})
#     print(f'[{r.status_code}] RULE ADDED: {json.dumps(r.json(), indent=2)}\n')
#     if r.status_code != 201: exit()
#
#     # GET STREAM RULES
#
#     r = api.request('tweets/search/stream/rules', method_override='GET')
#     print(f'[{r.status_code}] RULES: {json.dumps(r.json(), indent=2)}\n')
#     if r.status_code != 200: exit()
#
#     # START STREAM
#
#     r = api.request('tweets/search/stream', {
#             'expansions': EXPANSIONS,
#             'tweet.fields': TWEET_FIELDS,
#             'user.fields': USER_FIELDS,
#         },
#         hydrate_type=HydrateType.APPEND)
#
#     print(f'[{r.status_code}] START...')
#     if r.status_code != 200: exit()
#     for item in r:
#         print(json.dumps(item, indent=2))
#
# except KeyboardInterrupt:
#     print('\nDone!')
#
# except TwitterRequestError as e:
#     print(f'\n{e.status_code}')
#     for msg in iter(e):
#         print(msg)
#
# except TwitterConnectionError as e:
#     print(e)
#
# except Exception as e:
#     print(e)
