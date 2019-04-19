from fish import Fish
import random


#small test that will loop 100 times to make sure each output is as expected
#doesn't do much but neither does fish ¯\_(ツ)_/¯

for i in range(0,100):
    number = random.randint(0,20)

    fish = Fish(number)

    catch = fish.castLine()
        
    print (catch.toString())


