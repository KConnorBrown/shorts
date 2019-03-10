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
import markovify

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

def rename_sentences(full_data, Names):
    for i in range(0, len(full_data)):
        sentence = full_data[i][0]
        #find the proper names
        tokens = nltk.tokenize.word_tokenize(sentence.strip())
        tagged_sentence = nltk.tag.pos_tag(tokens)
        replace = []
        for j in range(0, len(tagged_sentence)):
            tag = tagged_sentence[j][1]
            word = tagged_sentence[j][0]
            if tag == 'NNP' or tag == 'NNPS':
                replace.append(word)
        replace = list(set(replace))
        for toReplace in replace:
            name = random.choice(Names)
            sentence = sentence.replace(toReplace.strip(), name)
        full_data[i][0] = sentence
        # print(full_data[i][0])
        # print('\n')


"""separates all the elements of each sentence into an list of arrays"""
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
    return extracted

def write_story(seed, text_model):
    with open('stories2.txt', 'a+') as s:
        # print(seed[0])
        s.write(seed[0] + ' ' + '\n')
    # Print five randomly-generated sentences
        for i in range(5):
            s.write(text_model.make_sentence() + ' ' + '\n')
            # print(text_model.make_sentence())
        # print('\n')
        # s.write('\n')
        s.write('\n')

def main():
    if not sentence_scraped: scrape_sentences()
    if not book_scraped: scrape_100years()
    if not name_parsed:
        book = open('100yrs.txt', 'r')
        names = get_names(book.read())
        book.close()
"""get the sentences and set of names ready"""
full_data = processTitleAuthorDataStrings()
n = open('names.txt', 'r')
names = n.readlines()
names = list(set(names))
# namesToSex = {}
for i in range(0,len(names)):
    names[i] = names[i].replace(",", "")
    names[i] = names[i].strip()

"""replace the names in the sentences with ones from the set of names
#full_data is a list of 4 tuple lists full_data[0][0] is "Call me Ishmael"
"""
rename_sentences(full_data, names)

# Build the model.
with open("100yrs.txt") as f:
    # Get raw text as string.
    text = f.read()
text_model = markovify.Text(text)
"""GENERATE 100 SHORT STORIES STARTING FROM A SEED"""

#clear stories file for testing purposes
with open('stories.txt', 'w') as s:
    s.write("")

while(len(full_data) > 0):
        seed = random.choice(full_data)
        full_data.remove(seed)
        write_story(seed, text_model) #seed is a list of format [renamed sentences, the Author, the Title of the book, and the date]




if __name__ == '__main__': main()
