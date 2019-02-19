import userData


class Person:
  def __init__(self, name,zipCode, age):
    self.name = name
    self.age = age
    self.zipCode = zipCode





def main():
  p1 = Person(userData.name, userData.zipCode, userData.age)
  print("The current user is",userData.name)
  print("This user is", userData.age, "years old")
  print("Their current zip code is", userData.zipCode)


main()

