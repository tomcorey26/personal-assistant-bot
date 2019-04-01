import random


# gets the species of the fish depending on the random number given
def getFish():
    fishID = random.randint(0, 20)

    # dictionary of fish that can be caught by the user
    fishSpecies = {1: "Trout", 2: "Salmon", 3: "Crayfish", 4: "Minnow", 6: "Lobster", 7: "Sardine", 8: "Mackerel",
                   5: "Boot", 9: "Finger", 0: "Seaweed"}

    # the default string for the wiki url
    wiki_url = "https://en.wikipedia.org/wiki/Loser_(hand_gesture)"

    # checks to see if the number generated is above 9, if it is above 9 there are no fish and the program will alert the user of their failure
    if (fishID > 9):
        fish = "You fail to catch a fish"
    else:

        # the fish is set to the corresponding dictionary key value
        fish = fishSpecies[fishID]

        # the wiki pages of each fish present in the program
        # also includes the joke wiki pages of finger boot and kelp
        if (fish == "Trout"):
            wiki_url = "https://en.wikipedia.org/wiki/Trout"
        elif (fish == "Salmon"):
            wiki_url = "https://en.wikipedia.org/wiki/Salmon"
        elif (fish == "Crayfish"):
            wiki_url = "https://en.wikipedia.org/wiki/Crayfish"
        elif (fish == "Minnow"):
            wiki_url = "https://en.wikipedia.org/wiki/Minnow"
        elif (fish == "Lobster"):
            wiki_url = "https://en.wikipedia.org/wiki/Lobster"
        elif (fish == "Sardine"):
            wiki_url = "https://en.wikipedia.org/wiki/Sardine"
        elif (fish == "Mackerel"):
            wiki_url = "https://en.wikipedia.org/wiki/Mackerel"
        elif (fish == "Boot"):
            wiki_url = "https://en.wikipedia.org/wikipa


def getFishString(fish, url):
    return ("You caught a " + fish + "!\nwikipedia url:\n" + url)


def main():
    # gets the random number to pass to the fishGame
    number = random.randint(0, 20)

    # stores the values from the fishGame when the getSpecies meathod is called
    fish, fish_wiki = getFish()

    # currently prints the output as a test to make sure the program works.
    print(getFishString(fish, fish_wiki))


if __name__ == "__main__":
    main()
