from pizzapi import *
from command_output import say
from input_converter import myCommand

#Change this variable based on a button press
input_type = "speech"

def initCustomer():
  import setup
  #get data from file
  order_info = setup.get_data()
  #if these things are not in the file, add them for future use
  if "first_name" not in order_info:
    order_info["first_name"] = input("First Name: ")
  if "last_name" not in order_info:
    order_info["last_name"] = input("Last Name: ")
  if "email" not in order_info:
    order_info["email"] = input("Email: ")
  if "phone" not in order_info:
    order_info["phone"] = input("Phone Number: ")
  if "address" not in order_info:
    order_info["address"] = input("Address: ")
  #update the file with the new info
  setup.write_data(order_info)
  #return customer data
  customer_info = Customer(order_info["first_name"], order_info["last_name"], order_info["email"], order_info["phone"])
  address_info = Address(order_info["address"], order_info["city"], order_info["state"], order_info["zip"])
  return customer_info, address_info

def printLocalStore(my_local_dominos):
  say("Your local dominos is:")
  say(my_local_dominos.get_details()['StreetName'])

def initOrder(customer_info, address_info):
  #find a local store
  try:
    my_local_dominos = address_info.closest_store()
  #if none are open, return nothing
  except:
    return

  printLocalStore(my_local_dominos)
  menu_data = my_local_dominos.get_menu()
  say("Starting order for your location...")
  order_info = Order(my_local_dominos, customer_info, address_info)

  return my_local_dominos, menu_data, order_info


def search_handler(menu_data, search):
  #create a dictionary for the options given the search criteria
  choices = {}
  #tokenize search criteria to separate words
  import nltk
  search_tokens = nltk.word_tokenize(search)
  #find the search criteria in the menu
  for v in menu_data.variants.values():
    if all(word in v['Name'].lower() for word in search_tokens):
      choices[v['Name']] = v['Code']
  #if the item is not in the list
  if len(choices) == 0:
    return "That item was not found on the menu"
  #return the only option
  if len(choices) == 1:
    return list(choices.values())[0]
  #multiple choices present
  else:
    say("Multiple choices detected.")
    ordered_choice = {}
    #create a dictionary with the choices numbered
    i = 1
    for key in choices.keys():
        ordered_choice[str(i)] = key
        i = i + 1
    while True:
      #have the user choose in the case of multiple options
      choice = ""
      if input_type == "speech":
        say("Which number do you want? ")
        print(str(ordered_choice))
        choice = myCommand()
      else:
        choice = input("Which number do you want? " + str(ordered_choice))
      if choice not in ordered_choice.keys():
        continue
      else:
        #return the product code
        return choices[ordered_choice[choice]]


def addtoOrder(order_info, menu_data):
  while True:
    confirm = ""
    if input_type == "speech":
      say("Would you like to add anything to your order? Yes or no? ")
      confirm = myCommand()
    else:
      confirm = input("Would you like to add anything to your order? (yes/no): ").lower()
    #keep adding to the order as long as the customer requests it
    if "yes" in confirm:
      search = ""
      if input_type == "speech":
        say("What would you like to add? ")
        search = myCommand()
        print(search)
      else:
        search = input("What do you want to add? ")
      #search for the item the customer wants
      item = search_handler(menu_data, search)
      #add it to the order
      try:
        order_info.add_item(item)
      #if it's not on the list, output it to the user
      except KeyError:
        say(item)
        continue
      continue
    #end the order
    elif "no" in confirm:
      return order_info
    else: continue

def initCard():
  card = input("Enter Credit Card Number: ")
  exp = input("Enter Expiration Date: ")
  security = input("Enter Security Code/CV: ")
  billing = input("Enter Billing Zip Code: ")

  card = PaymentObject(card, exp, security, billing)

  return card


def main():
  #Get customer information
  customer_info, address_info = initCustomer()

  #Find local Domino's, get menu, and begin order
  try:
    my_local_dominos, menu_data, order_info = initOrder(customer_info, address_info)
  #if no local Domino's is open, report this to the user
  except TypeError:
    return "No local stores are currently open."

  #Search for items from menu and add to order
  order_info = addtoOrder(order_info, menu_data)
  #display the user's order
  say("Here is your order: ")
  print(order_info.data['Products'])
  #If nothing in the order, end the process
  if len(order_info.data ['Products']) == 0: return "Order empty. Have a nice day!"

  #Choose between pick up or delivery
  if input_type == "speech":
    say("Carryout or delivery? ")
    option = myCommand()
    if option.lower() == "carry out":
      order_info.changeToCarryout()
  else:
    option = input("Carryout or Delivery (c/d): ")
    if option == 'c':
      order_info.changeToCarryout()

  #Get credit card information
  card = initCard()

  #place the order
  # order_info.place(card)
  # my_local_dominos.place_order(order_info, card)
  # Uncomment these to actually place order

  return "Order complete! It should arrive soon."


if __name__== "__main__":
  main()
