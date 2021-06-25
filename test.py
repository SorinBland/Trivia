import json
import urllib.request

from requests import get

categories = {}
questions_list = []
correct_answers = []
incorrect_answers = []


def start_game():
    categories_t = get("https://opentdb.com/api_category.php")
    data = json.loads(categories_t.content)

    for cat in data['trivia_categories']:
        categories[cat["id"]] = cat['name']


start_game()
key_list = list(categories.keys())
val_list = list(categories.values())
key = val_list.index("General Knowledge")

url = "https://opentdb.com/api.php?amount=10&category=9&difficulty=easy"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

for q in data['results']:
    questions_list.append(q['question'])
    correct_answers.append(q['correct_answer'])
    incorrect_answers.append(q['incorrect_answers'])

# print(questions_list)
# print(incorrect_answers)
# print(correct_answers)
# for elem in correct_answers:
#     print(elem.split(","))

lista = ["1", "2", "3"]

count = 0

while count < 3:
    count += 1
    print(count)
