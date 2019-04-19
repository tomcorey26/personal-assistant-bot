import random

class Fish():

    def __init__(self, number):
        
        #dictionary of fish that can be caught by the user
        self.speciesList = {1:"Trout",2:"Salmon", 3:"Crayfish", 4:"Shark", 6:"Lobster", 7:"Sardine", 8:"Mackerel", 5:"Boot", 9:"Crab", 0:"Seaweed"}
        
        #the random number generated when ran
        self.number = number
        self.species, self.wiki_url = self.getSpecies()
        


    #gets the species of the fish depending on the random number given
    def getSpecies(self):
        
        #the default string for the wiki url
        wiki_url = ""
        
        #checks to see if the number generated is above 9, if it is above 9 there are no fish and the program will alert the user of their failure
        if(self.number > 9):
            fish = "You fail to catch a fish"
            wiki_url = "https://en.wikipedia.org/wiki/Loser_(hand_gesture)"
            
        else:
            #the fish is set to the corresponding dictionary key value
            fish = self.speciesList[self.number]
            if(fish == "Crab"):
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                wiki_url = "https://www.youtube.com/watch?v=pwSsT8IU0WE"
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
                #🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀
            else:
                wiki_url = "https://en.wikipedia.org/wiki/" + fish
            
        #returns the caught fish and the url to the user
        return fish, wiki_url

    def toString(self):
        #return the fish species and url in string form
        if self.number > 9:
            output_string = self.species
        else:
            output_string = "You caught a " + self.species + "!\n" + self.wiki_url

        return output_string

    def castLine(self):
        catch = Fish(self.number)
        return catch

def main():

    number = random.randint(0,20)
    fish = Fish(number)
    #gets the random number to pass to the fishGame
    catch = fish.castLine()
    
    #returns a string of 
    print (catch.toString())

if __name__ == "__main__":
    main()
