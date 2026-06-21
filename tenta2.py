#del1 
#uppgift1
#1.1
import random

def dice_rolls_until(sides, target):
    summa = 0
    lista = []
    while summa < target:
        diceroll = random.randint(1,sides)
        summa += diceroll
        lista.append(diceroll)
    return lista

# print(dice_rolls_until(6, 100))

def count_pairs(lst):
    antal = 0

    for i in range(len(lst)-1):

        if lst[i] == lst[i+1]:

            # inte samma före
            if i == 0 or lst[i] != lst[i-1]:

                # inte samma efter
                if i == len(lst)-2 or lst[i] != lst[i+2]:
                    antal += 1

    return antal
        


print(count_pairs([3.3, 3.3, '1', 'a', 'a']))

