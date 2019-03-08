import requests
from bs4 import BeautifulSoup
import string
import random
first_sentence_url = 'http://americanbookreview.org/100BestLines.asp' #sentences url
text_url = 'https://archive.org/stream/OneHundredYearsOfSolitude_201710/One_Hundred_Years_of_Solitude_djvu.txt' #link to text of 100 yrs of solitude
sentence_scraped = True #very gross check
# archetypes = ["tragedy", "comedy"]
book_scraped = True
name_parsed = True
import nltk
from nameparser.parser import HumanName

def scrape_sentences():
    sentencesHTML = open('sentences.html', 'w+')
    for l in (requests.get(first_sentence_url)).text: sentencesHTML.write(l)
    sentencesHTML.close()
    sentencesHTML = open('sentences.html', 'r')
    soup = BeautifulSoup(sentencesHTML, features='html.parser')
    sentencesTXT = open('raw.txt', 'w+')
    for l in soup.get_text():
        sentencesTXT.write(l)
    sentencesTXT.close()

def scrape_100years():
    soup = BeautifulSoup(requests.get(text_url).text, features='html.parser')
    book = open("100yrs.txt", 'w+')
    for l in soup.get_text():
        book.write(l)
    book.close()

def get_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)

def extract_auth(l):
    l = l.strip()
    mapped = []
    temp = l
    i = len(l)-1
    dated = False
    if (i > 0):
        while (i > 0) :
            #date
            if l[i] == ')' and not dated:
                dated = True
                date = temp[i-4:i]
                mapped = [date] + mapped
                temp = l
                i = i-6

                #title
                assert(l[i] == " "), "not a space"
                while(l[i] == " "):
                    i = i - 1
                    j = i
                while(l[j] != ","):
                    j = j - 1
                title = temp[j+2:i+1]
                title = title.strip()
                mapped = [title] + mapped
                temp = l
                i = j

                #Author
                while(l[j] != "—"):
                    j = j - 1
                author = temp[j+1:i]
                mapped = [author] + mapped
                i = j
                temp = l

                #first sentence
                while i > 0:
                    if l[i] == "." or l[i] == "?" or l[i] == "!" or l[i] == '""':
                        sentence = temp[:i+1]
                        mapped = [sentence] + mapped
                        break;
                    i = i - 1
            i = i - 1

    return mapped

"""extract authors, titles, dates and map them to the first sentences
each data is a list of these 4 items

eg:

['Justice?—You get justice in the next world, in this world you have the law.', 'William Gaddis', 'A Frolic of His Own', '1994']
 """
def processTitleAuthorDataStrings():
    s = []
    sents = open('sentences.txt', 'r')
    for l in sents.readlines():
        l = l[4:] #get rid of numbering 1-100
        s.append(l)
    sents.close()
    extracted = []
    for sent in s:
        data = extract_auth(sent)
        extracted.append(data)
    return s

def write_story(seed):
    return;

def main():
    if not sentence_scraped: scrape_sentences()
    if not book_scraped: scrape_100years()
    if not name_parsed :
        book = open('100yrs.txt', 'r')
        names = get_names(book.read())
        book.close()

"""get the sentences and set of names ready"""
    sentences = processTitleAuthorDataStrings()
    n = open('names.txt', 'r')
    names = n.readlines()
    names = list(set(names))
    for i in range(0,len(names)):
        names[i] = names[i].replace(",", "")
        names[i] = names[i].strip()
    # print(names) <-- gives an array of names in the book with no repeats
    # print(len(names))

"""GENERATE 100 SHORT STORIES STARTING FROM A SEED"""
    while(len(sentences > 0):
        seed = random.choice(sentences)
        sentences.remove(seed)
        write_story(seed)



if __name__ == '__main__': main()
