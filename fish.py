import random

class Fish():

    def __init__(self, number):
        #the random number generated when ran
        self.number = number
        #dictionary of fish that can be caught by the user
        self.fishSpecies = {1:"Trout",2:"Salmon", 3:"Carp", 4:"Goldfish", 6:"Catfish", 7:"Atlantic Cod", 8:"Haddock", 5:"Boot", 9:"Finger", 0:"Kelp"}
    #gets the species of the fish depending on the random number given
    def getSpecies(self):
        #the default string for the wiki url
        wiki_url = ""
        #checks to see if the number generated is above 9, if it is above 9 there are no fish and the program will alert the user of their failure
        if(self.number > 9):
            fish = "You fail to catch a fish"
        else:
            #the fish is set to the corresponding dictionary key value
            fish = self.fishSpecies[self.number]
            #the wiki pages of each fish present in the program
            #also includes the joke wiki pages of finger boot and kelp
            if(fish == "Trout"):
                wiki_url = "https://en.wikipedia.org/wiki/Trout"
            elif(fish == "Salmon"):
                wiki_url = "https://en.wikipedia.org/wiki/Salmon"
            elif(fish == "Carp"):
                wiki_url = "https://en.wikipedia.org/wiki/Carp"
            elif(fish == "Goldfish"):
                wiki_url = "https://en.wikipedia.org/wiki/Goldfish"
            elif(fish == "Catfish"):
                wiki_url = "https://en.wikipedia.org/wiki/Catfish"
            elif(fish == "Atlantic Cod"):
                wiki_url = "https://en.wikipedia.org/wiki/Atlantic_cod"
            elif(fish == "Haddock"):
                wiki_url = "https://en.wikipedia.org/wiki/Haddock"
            elif(fish == "Boot"):
                wiki_url = "https://en.wikipedia.org/wiki/Boot"
            elif(fish == "Finger"):
                wiki_url = "https://en.wikipedia.org/wiki/Finger"
            elif(fish == "Kelp"):
                wiki_url = "https://en.wikipedia.org/wiki/Kelp"
        #returns the caught fish and the url to the user
        return fish, wiki_url


def main():
    #gets the random number to pass to the fishGame
    number = random.randint(0,20)
    #instantiates a new Fish object fishGame and gives it a number to use for the dictionary key
    fishGame = Fish(number)
    #stores the values from the fishGame when the getSpecies meathod is called
    fish, fish_wiki = fishGame.getSpecies()
    #currently prints the output as a test to make sure the program works.
    print(fish)
    print(fish_wiki)

if __name__ == "__main__":
    main()

