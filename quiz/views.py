import json
import random
import urllib.request
from django.shortcuts import render, redirect
from requests import get
from quiz.forms import QForm
from quiz.models import Questions, Player, CAnswers, IAnswers

categories = {}
DIFFICULTY = ("easy", "medium", "hard")
MAX_QUESTIONS = 15
CATEGORIES_URL = "https://opentdb.com/api_category.php"
questions_list = []
correct_answers = []
incorrect_answers = []


def select_choices(request):
    try:
        Player.objects.all().delete()
        Questions.objects.all().delete()
        CAnswers.objects.all().delete()
        IAnswers.objects.all().delete()

        categories_t = get(CATEGORIES_URL)
        data = json.loads(categories_t.content)

        for cat in data['trivia_categories']:
            categories[cat["id"]] = cat['name']

        return render(request, 'index.html', {"max_questions": MAX_QUESTIONS, "categories": categories,
                                              'difficulty': DIFFICULTY})
    except ValueError:
        return render(request, 'error_page.html')


def start_game(request):
    max_questions = request.POST.get('quantity')
    category = str(request.POST.get('category'))
    difficulty = request.POST.get("difficulty")

    key_list = list(categories.keys())
    val_list = list(categories.values())
    key = val_list.index(f"{category}")

    questions_api = f"https://opentdb.com/api.php?amount={max_questions}&category={key_list[key]}&" \
                    f"difficulty={difficulty}"
    response = urllib.request.urlopen(questions_api)
    data = json.loads(response.read())

    if data['response_code'] == 1:
        return render(request, 'error_page.html')

    for item in data['results']:
        questions_list.append(item['question'])
        correct_answers.append(item['correct_answer'])
        incorrect_answers.append(item['incorrect_answers'])

    for question in questions_list:
        Questions.objects.create(question=question)

    for correct_answer in correct_answers:
        CAnswers.objects.create(correct_answer=correct_answer)

    for incorrect_answer in incorrect_answers:
        str_incanswers = ",".join([str(word) for word in incorrect_answer])
        IAnswers.objects.create(incorrect_answer=str_incanswers)

    request.session['max'] = max_questions
    Player.objects.create(current_question=0, score=0)

    return redirect('in_game')


def in_game(request, new_player=Player.objects.last()):
    # try:
    max = request.session['max']
    score = new_player.score
    new_player.current_question += 1
    if new_player.current_question <= int(max):
        questions_game = Questions.objects.all()
        question_now = questions_game[new_player.current_question - 1]

        all_answers = []
        canswer = CAnswers.objects.all()
        c_answer_now = canswer[new_player.current_question - 1]

        incanswers = IAnswers.objects.all()
        i_answer_now = incanswers[new_player.current_question - 1]
        all_answers.append(c_answer_now.correct_answer)

        for word in i_answer_now.incorrect_answer.split(","):
            all_answers.append(word)

        random.seed(random.randint(1, 4))
        random.shuffle(all_answers)

        form = QForm(request.POST)
        if request.method == 'POST' or request.method == 'GET':
            form = QForm(request.POST)
            if form.is_valid():
                answer = form['answer'].value()
                if str(answer) == str(canswer[new_player.current_question - 2]):
                    new_player.score += 1
                return render(request, 'game.html',
                              {'form': form, 'question': question_now, 'all_answers': all_answers,
                               "new_player": new_player, 'max': max})
            return render(request, 'game.html', {'form': form, 'question': question_now, 'all_answers': all_answers,
                                                 "new_player": new_player, 'max': max})
        return render(request, 'game.html', {'form': form, 'question': question_now, 'all_answers': all_answers,
                                             "new_player": new_player, 'max': max})

    new_player.score = 0
    new_player.current_question = 0
    questions_list.clear()
    correct_answers.clear()
    incorrect_answers.clear()

    return render(request, 'game_over.html', {'score': score, 'max': max})
    # except AttributeError:
    #     return render(request, 'error_page.html')