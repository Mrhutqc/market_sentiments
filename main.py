from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import datetime
import pandas as pd
import re
from textblob import TextBlob
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class SentimentWatcher:
    def __init__(self):
        self.tweets = pd.DataFrame(columns=["tweets"])
        o = TwitterOAuth.read_file()
        self.api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')
        self.positive_tweets = None
        self.negative_tweets = None

    # api = Api(bearer_token=bearer_token)
    # Compute The Negative, Neutral, Positive Analysis
    @staticmethod
    def analysis(score):
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"

    # Clean The Data
    @staticmethod
    def cleantext(text) -> str:
        text = re.sub(r"@[A-Za-z0-9]+", "", text)  # Remove Mentions
        text = re.sub(r"#", "", text)  # Remove Hashtags Symbol
        text = re.sub(r"RT[\s]+", "", text)  # Remove Retweets
        text = re.sub(r"https?:\/\/\S+", "", text)  # Remove The Hyper Link

        return text

    # Get The Subjectivity
    @staticmethod
    def sentiment_analysis(ds):
        sentiment = TextBlob(ds["tweet"]).sentiment
        return pd.Series([sentiment.subjectivity, sentiment.polarity])

    def clear_rules(self):
        try:
            # GET STREAM RULES
            rule_ids = []
            r = self.api.request('tweets/search/stream/rules', method_override='GET')
            for item in r:
                if 'id' in item:
                    rule_ids.append(item['id'])
                else:
                    print(json.dumps(item, indent=2))

            # DELETE STREAM RULES

            if len(rule_ids) > 0:
                r = self.api.request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
                print(f'[{r.status_code}] RULES DELETED: {json.dumps(r.json(), indent=2)}\n')

        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    def add_rules(self):
        try:
            QUERY = "from:elonmusk OR from:IOHK_Charles OR from:el_billy1 BTC OR from:Mrhutqc BTC"

            # ADD STREAM RULES
            r = self.api.request('tweets/search/stream/rules', {'add': [{'value': QUERY}]})

            print(f'[{r.status_code}] RULE ADDED: {r.text}')
            if r.status_code != 201:
                exit()

        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    def start_watching(self):
        try:
            # GET STREAM RULES
            r = self.api.request('tweets/search/stream/rules', method_override='GET')
            print(f'[{r.status_code}] RULES: {r.text}')
            if r.status_code != 200:
                exit()

            # START STREAM
            r = self.api.request('tweets/search/stream')
            print(f'[{r.status_code}] START...')
            if r.status_code != 200:
                exit()

            for item in r:
                print(item)

                new_tweet = pd.Series(item['data']['text'])



                # self.tweets = pd.concat([self.tweets, new_tweet], ignore_index=True)
                print(new_tweet)
                # tweets = pd.concat([self.tweets, new_tweet])
                # print(item)

        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    def clean_tweets(self):
        # Clean The Text
        self.tweets["tweet"] = self.tweets["tweet"].apply(self.cleantext)

    def add_sentiment_analysis_to_dataframe(self):
        # Adding Subjectivity & Polarity
        self.tweets[["subjectivity", "polarity"]] = self.tweets.apply(self.sentiment_analysis, axis=1)

    def generate_words_cloud(self):
        allwords = " ".join([twts for twts in self.tweets["tweet"]])
        wordCloud = WordCloud(width=1000, height=1000, random_state=21, max_font_size=119).generate(allwords)
        plt.figure(figsize=(20, 20), dpi=80)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        # Create a New Analysis Column
        self.tweets["analysis"] = self.tweets["polarity"].apply(self.analysis)
        # Print The Data

    def get_positive_negative_tweets(self):
        self.positive_tweets = self.tweets[self.tweets['analysis'] == 'Positive']
        self.negative_tweets = self.tweets[self.tweets['analysis'] == 'Negative']
        print(len(self.positive_tweets) / len(self.negative_tweets))

    def plot_doted_graph(self):
        plt.figure(figsize=(10, 8))
        for i in range(0, self.tweets.shape[0]):
            plt.scatter(self.tweets["polarity"][i], self.tweets["subjectivity"][i], color="Red")
        plt.title("Sentiment Analysis")  # Add The Graph Title
        plt.xlabel("Polarity")  # Add The X-Label
        plt.ylabel("Subjectivity")  # Add The Y-Label
        plt.show()  # Showing The Graph
        print("done")


if __name__ == "__main__":
    watcher = SentimentWatcher()
    watcher.start_watching()

