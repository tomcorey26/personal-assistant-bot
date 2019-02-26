import random as rand
import time


class SalmonFisher():

    def __init__(self, number):
        self.number = number
    
    def fishForSalmon(self):

        print("Welcome to fishing with the salmon slasher")


        for i in range(100000):

            self.number = rand.randint(0,10000)

            print("You have not caught a salmon :( ")

            if(self.number == 1):

                print("You have not caught a salmon :(. but you did catch a fish. You had to throw it back.")
            
            elif(self.number == 100):
                print("you have caught a salmon! Congrats!")
                time.sleep(10)
                print("But you also played this salmon game for an hour... so are you really a winner?")
                break

            time.sleep(2.16)
        print("You did not catch a single salmon in an hour of fishing!")
        

def main():

    number = rand.randint(0,100000)

    fishGame = SalmonFisher(number)

    fishGame.fishForSalmon()
    
main()