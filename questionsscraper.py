import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


headers = {"Accept-Language": "en-US, en;q=0.5"}

#data storage
questions = []
options = []
answers = []
anki_fronts = []
links =[]


# input url to site like https://vceguide.com/comptia/cv0-002-comptia-cloud/page/X/") and it returns a list of direct urls to questions
def LinksGrabber(url):
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")
    questions_art = soup.find_all('article')

    for article in questions_art:
        link = article.h1.a.get('href')
        links.append(link)
    return links


def QuestionListCreation(url):
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")
    content_div = soup.find('div', class_='entry-content')
    question = content_div.p.text.splitlines()[0]
    options_list = []
    for line in content_div.p.select('strong'):
        if line.text.startswith('Correct'):
            answer = line.text
            break
        options_list.append(line.text)
    questions.append(question)
    options.append(options_list)
    anki_fronts.append(question)
    anki_fronts.append(options)
    answers.append(answer)


# Getting all url in one list - lists
for i in range(1,14):
    LinksGrabber(f"https://vceguide.com/comptia/cv0-002-comptia-cloud/page/{i}/")

for link in links:
    QuestionListCreation(link)

questions = pd.DataFrame({
    'question': questions,
    'options': options,
    'answer': answers
})

#print(questions)

#questions.to_csv('cloud_questions.csv')

anki_cards = pd.DataFrame({
    'front': anki_fronts,
    'back': answers
})

anki_cards.to_csv('anki_cloud.csv')