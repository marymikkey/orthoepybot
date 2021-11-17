import random
from random import randint
from random import randrange

#обрабатываем список заданий 2
f3= open('zadka2.txt', 'r')
lines = f3.readlines()
lines = [line.rstrip() for line in lines]

words = []
ans2 = []
for line in lines:
    for word in line:
        if not word.isalpha():
            line = line.replace('|', '')
    words.append(line)

print(words)

#обрабат спис ответов

linepart1 = ()
linepart2 = ()
for line in lines:
        x2 = line.find('|')+1
        linepart1 = line[: x2]
        linepart2 = line[x2 : ]
        linepart2 = linepart2.capitalize()
        line = linepart1.replace('|', '') + linepart2
        ans2.append(line)
print(ans2)
print(answers[i])
print(explanations[i])