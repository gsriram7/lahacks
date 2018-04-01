from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import json
import math

credentials = service_account.Credentials.from_service_account_file('apikey.json')

scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

tickers = {}

with open("tickers_to_wiki.json", 'r') as fp:
    tickers = dict(json.load(fp))
fp.close()

def get_sentiment(company_name, text):
    client = language.LanguageServiceClient(credentials=credentials)
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    s_analysis = client.analyze_sentiment(document=document)
    score = s_analysis.document_sentiment.score
    magnitude = s_analysis.document_sentiment.magnitude

    word_count = len(text.split())

    normalized_magnitude = magnitude / (27 + word_count)

    e_analysis = client.analyze_entity_sentiment(document=document)
    entities = list([e for e in e_analysis.entities])

    index = len(entities) - 1

    wiki_url = tickers[company_name]

    entity_score = 0
    entity_magnitude = 0

    has_entity = False

    for idx, e in enumerate(entities):
        if e.metadata['wikipedia_url'] == wiki_url:
            index = idx
            entity_score = e.sentiment.score
            entity_magnitude = e.sentiment.magnitude
            print(e.metadata['wikipedia_url'])
            has_entity = True
            break

    normalized_entity_magnitude = entity_magnitude / (27 + word_count)

    relevance_score = (len(entities) - index) / len(entities)

    entity_sentiment = entity_score * normalized_entity_magnitude * relevance_score

    if has_entity and entity_sentiment!=0:
        print('Has entity')
        return entity_sentiment
    else:
        print('No entity')
        penalty = 0.00001
        if has_entity:
            penalty = 1
        return score * normalized_magnitude * relevance_score * penalty

if __name__ == '__main__':
    example1 = "Donald Trump announces that Amazon will be banished to the Amazon Jungle"
    example2 = 'Apple\'s presentation for its new iPad for classrooms pulled lessons from Steve Jobs https://t.co/ktsIlZRv3u,The crazy thing isn’t how big Apple’s dividend hikes consistently are. The crazy thing is that, as fast as it lifts… https://t.co/yrpqmHlBHx,1976 - Apple Inc. is formed by Steve Jobs, Steve Wozniak, and Ronald Wayne in Cupertino, California, USA'
    example3 = 'Apple iphone is very bad as the battery is terrible'
    example4 = "Apple iphone is very bad and has a terrible battery. Use Samsung instead, it has a great battery life, amazing screen. You are sure to love it because it is very good"
    example5 = 'Apple stocks are going up, good news for Apple. Great! #Apple #comeback'
    example6 = 'Apple sucks!'
    example7 = '4th time forced into Windows update that messes up my computer in the last 4 days. I\'m so annoyed. #Windows10 #microsoft'
    company_name = 'MSFT'

    examples = [example1, example2, example3, example4]

    # for e in examples:
        # print(get_sentiment(company_name, e))

    print(get_sentiment(company_name, example7))


def get_average_sentiment(all_tweets):
    company_name = all_tweets['company']
    tweets = all_tweets['tweets']
    total = 0
    tot_follow = 0

    if not tweets or company_name not in tickers:
        return 0

    for t in tweets:
        sentiment = get_sentiment(company_name, t['text'])
        tot_follow += t['followers']
        total += (sentiment * (math.pow(t['followers'], 0.9) * (t['retweets'] * 0.2 + 150)))

    average = total / (math.pow(tot_follow, 0.71) + len(tweets)*150)

    return {"company": company_name, "sentiment": average}
