import random
from django.shortcuts import render, redirect
import requests
from .models import Game, Attempt

def home(request):
    if request.method == 'POST':
        guess = request.POST['guess'].upper()
        game_id = request.session.get('game_id')
        game = Game.objects.get(id=game_id)
        
        if len(guess) != 5 or not is_valid_word(guess):
            error_message = 'Word not in the dictionary' if len(guess) == 5 else 'Please enter a 5-letter word'
            return render(request, 'wordle_app/index.html', {'error': error_message, 'grid': get_grid(game)})

        colors = calculate_colors(guess, game.word)
        Attempt.objects.create(game=game, guess=guess, colors=colors)
        game.attempts += 1
        game.save()

        if guess == game.word:
            return render(request, 'wordle_app/success.html', {'word': game.word, 'attempts': game.attempts})
        
        if game.attempts >= 6:
            return render(request, 'wordle_app/failure.html', {'word': game.word, 'attempts': game.attempts})
        
        return render(request, 'wordle_app/index.html', {'grid': get_grid(game)})

    word = get_random_word()
    game = Game.objects.create(word=word)
    request.session['game_id'] = game.id
    return render(request, 'wordle_app/index.html', {'grid': get_grid(game)})

def is_valid_word(word):
    url = f"https://api.datamuse.com/words?sp={word.lower()}&max=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data) > 0 and data[0]['word'] == word.lower()
    return False

def calculate_colors(guess, word):
    colors = ''
    for i, letter in enumerate(guess):
        if letter == word[i]:
            colors += 'G'  # Green
        elif letter in word:
            colors += 'Y'  # Yellow
        else:
            colors += 'B'  # Grey
    return colors

def get_grid(game):
    attempts = Attempt.objects.filter(game=game).order_by('created_at')
    grid = [[{'letter': '', 'color': ''} for _ in range(5)] for _ in range(6)]
    for i, attempt in enumerate(attempts):
        for j, letter in enumerate(attempt.guess):
            grid[i][j] = {'letter': letter, 'color': get_color(attempt.colors[j])}
    return grid

def get_color(color_code):
    if color_code == 'G':
        return 'green'
    elif color_code == 'Y':
        return 'yellow'
    else:
        return 'gray'

def get_random_word():
    WORDS = ['APPLE', 'BERRY', 'CHESS', 'DRIVE', 'EAGLE', 'FANCY', 'GIANT', 'HOUSE', 'INPUT', 'JOKER']
    return random.choice(WORDS)
