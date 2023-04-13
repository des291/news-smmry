from bs4 import BeautifulSoup
import requests
import json
import nltk
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

lsa = LsaSummarizer(Stemmer('english'))
lsa.stop_words = get_stop_words('english')
luhn = LuhnSummarizer(Stemmer('english'))
luhn.stop_words = get_stop_words('english')


class ReadRss:

    def __init__(self, rss_url, headers, name):

        self.name = name
        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, 'lxml')
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)
        self.articles = self.soup.findAll('item')
        self.articles_json = 0
        self.articles_dicts = [{'title': a.find('title').text, 'link': a.link.next_sibling.replace('\n', '').replace(
            '\t', ''), 'description': a.find('description').text, 'pubdate': a.find('pubdate').text} for a in self.articles]
        self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
        self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
        self.descriptions = [d['description']
                             for d in self.articles_dicts if 'description' in d]
        self.pub_dates = [d['pubdate']
                          for d in self.articles_dicts if 'pubdate' in d]


def to_json(articles, path):
    with open(path, 'w') as file:
        json.dump(articles, file)


bbc = ReadRss('https://feeds.bbci.co.uk/news/rss.xml?edition=uk',
              headers, 'bbc')
# print(bbc.articles_dicts)
# with open('bbc.json', 'w') as file:
#     json.dump(bbc.articles_dicts, file)
# print(bbc.articles_dicts)
# bbc.to_json()

guardian = ReadRss('https://www.theguardian.com/uk/rss', headers, 'guardian')
# print(guardian.articles_dicts)
# guardian.to_json()

independent = ReadRss(
    'https://www.independent.co.uk/news/rss', headers, 'independent')
# print(independent.articles_dicts)
# independent.to_json()


def get_BBC_articles(urls):
    articles = []
    i = 0
    while len(articles) < 7:
        print(i)
        try:
            r = requests.get(urls[i])
        except IndexError:
            break
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('h1').get_text()
        if urls[i][22:26] == 'news':
            paragraphs = soup.find_all(
                'p', "ssrcss-1q0x1qg-Paragraph eq5iqo00")
        else:
            paragraphs = soup.find_all(
                'span', attrs={'data-reactid': re.compile(r"paragraph-")})
        text = [sentence.get_text() for sentence in paragraphs]
        if urls[i][22:26] == 'news':
            text = text[1:-4]
        text = ' '.join(text)
        if text == '':
            i += 1
            continue
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        summary = []
        # for sentence in list(lsa(parser.document, 7)):
        #     summary.append(sentence._text)
        for sentence in list(luhn(parser.document, 7)):
            summary.append(sentence._text)
        article = {
            "title": title,
            "text": text,
            "url": urls[i],
            "summary": summary
        }
        articles.append(article)
        i += 1
    return articles


bbc_articles = get_BBC_articles(bbc.urls)
bbc_sport = ReadRss(
    'https://feeds.bbci.co.uk/sport/rss.xml?edition=uk', headers, 'bbc_sport')
bbc_sport_articles = get_BBC_articles(bbc_sport.urls)
# test = get_BBC_articles(
# ['https://www.bbc.co.uk/sport/football/61636938?at_medium=RSS&at_campaign=KARANGA'])
to_json(bbc_articles, 'data/bbc.json')
to_json(bbc_sport_articles, 'data/bbc-sport.json')
# to_json(test, 'data/bbc.json')
# parser = PlaintextParser.from_string(
#     bbc_articles[0]['text'], Tokenizer('english'))
# summary = list(lsa(parser.document, 7))
# print(dir(summary[0]))
