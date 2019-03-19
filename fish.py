import random as random

class Fish():

    def __init__(self, number):
        self.number = number
        self.fishSpecies = {1:"Trout",2:"Salmon", 3:"Carp", 4:"Gold Fish", 6:"Catfish", 7:"Atlantic Cod", 8:"Haddock", 5:"Boot", 9:"Finger", 0:"Kelp"}

    def getSpecies(self):
        if(self.number > 9):
            fish = "You fail to catch a fish"
        else:
            fish = self.fishSpecies[self.number]
        return fish


def main():

    number = random.randint(0,20)

    fishGame = Fish(number)

    fish = fishGame.getSpecies()

    print(fish)

main()

