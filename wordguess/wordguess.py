import random

print('Welcome')
print('Type y in start to start guessing the word')
print('You have a limited amount of guesses which depends upon the word')
print('After each guess you are shown on the right, which letters were guessed correct')
print('If a letter was in the correct position, it will be capital')
print('If a letter was in the word but not in correct position, it will be small')
print()

with open('words.txt','r') as file:
    l = file.readlines()    

while True:
    s = input('Start(y/n):')
    if s != 'y':
        break
    word = random.choice(l)[:-1]
    word = 'mountain'
    n = len(word)
    print(n,'words')
    print('.'*n)
    guesses = len(word) + len(word)//3
    guessed = False  
    while not guessed:
        tab = list(word)
        print('\t\t','Guesses left:',guesses)
        if guesses == 0:
            print('You did not guess the correct word')
            break
        g = input('Guess:')
        g = g.lower()
        if g == word:
            print('You guessed correct')
            break
        elif len(g) != n:
            print('Incorrect Lenght')
            continue
        cut = ''
        won = True
        for i in range(len(g)):
            if g[i] == word[i]:
                cut += g[i].upper()
                if tab[i] == '_':
                    cut = cut[-1::-1].replace(word[i],'.',1)[-1::-1]
            elif g[i] in tab:
                cut += g[i].lower()
                i = tab.index(g[i])
            else:
                cut += '.'
            tab[i] = '_'            
        print('\t\t',cut)
        guesses -= 1
        
