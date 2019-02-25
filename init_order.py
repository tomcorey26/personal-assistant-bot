from pizzapy import *

# #create init function that starts it all

# #TODO make this into a function
# #error handling
def initCustomer():
  firstName = input("First Name: ")
  lastName = input("Last Name: ")
  email = input ("Email: ")
  number = input ("Phone number: ")
  address = input ("Address: ")
  print("\n")

  customer = Customer(firstName, lastName, email, number, address)

  return customer

def initOrder(customer):
  my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)




def printDominos(my_local_dominos):
  print("Your local dominos is: \n")
  print(my_local_dominos)

menu = my_local_dominos.get_menu()

order = Order.begin_customer_order(customer, my_local_dominos)

search = ''


# #TODO make function for order
# #TODO have error handling for order
# #make recursive to repeat order?
# #make loop completely stop when done is entered
#added functions
while search != 'done':
  search = input("Search for item (Enter 'done' to exit): ")
  print("Search results for " + search)
  print("\n")
  menu.search(Name=search)
  print("\n")
  
  confirm = input("Would you like to add anything to your order? (y/n): ")
  if confirm == 'y':
    item = input('Enter the code of the item you would like to add: ')
    order.add_item(item)

print("Here is your order: ")
print(order.data['Products'])

card = input("Enter credit card number: ")
exp = input("Enter expiration: ")
security = input("Enter Security code: ")
billing = input("Enter billing ZIP: ")

card = CreditCard(card, exp, security, billing)

option = input("Carryout or Delivery (c/d): ")
if option == 'c':
  order.changeToCarryout()

# Uncomment these to actually place order

# order.place(card)

# my_local_dominos.place_order(order, card)

def main():
  customer = initCustomer()
  print("test")


if __name__== "__main__":
  main()
