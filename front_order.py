from pizzapy import *

class Pizza:
  def __init__(self,customer):
    self.customer = customer
    print("set customer")
    self.store = StoreLocator.find_closest_store_to_customer(self.customer)
    print("found store")
    self.menu = self.store.get_menu()
    print("got menu")
    
    self.order = Order.begin_customer_order(self.customer,self.store)
    print("began order")

  def addtoOrder(self,item):
    self.order.add_item(item)  
    return order
  
  def addFromArr(self,arr):
    for item in arr:
      self.order.add_item(item)
  
  def changeToPickup(self):
    self.order.data['ServiceMethod'] = 'Carryout'
    return
  
  def changeToDeliv(self):
    self.order.data['ServiceMethod'] = 'Delivery'
    return
  
  def placeOrder(self,card):
    self.order.place(card)
    self.store.place_order(self.order,card)

    return order
  
  #////////////////////////////////////
  #Functions below this are for testing
  #////////////////////////////////////

  def testOrder(self,card):
    self.order.pay_with(card)
    return

  def printStore(self):
    print(self.store)
    return

  def printOrder(self):
    print(self.order)
    return
  
def main():

  #create customer instance made from kivy inputs or stored information
  customer = Customer("tom","corey","tomcorey26@gmail.com","401999999","39 Joy Lane, Rhode Island, 02882")

  print("created customer")
  
  #create instance of pizza by passing it new customer object
  #takes care of finding store,menu, and starting order in constructor
  pizza = Pizza(customer)

  print("created pizza object")
  
  #Have an array that stores the codes of the items user added to order
  arrayOfItemCodes = ['P12IPAZA','MARINARA','20BCOKE']
  print("added item codes")

  #this method loops through an array of item codes and adds them to the order object
  #could run when button is clicked
  pizza.addFromArr(arrayOfItemCodes)
  print("added item codes")
  
  pizza.printOrder()

  #Have a button for each of these methods
  pizza.changeToPickup()
  pizza.changeToDeliv()

  print(pizza.order.data['ServiceMethod'])
  print(pizza.order.store)

  #create card instace from kivy input
  card = CreditCard("","","","")

  #Place order button that runs this
  #pizza.placeOrder(card)
  #pizza.testOrder(card)

  #pizza.menu.display()

if __name__== "__main__":
  main()
