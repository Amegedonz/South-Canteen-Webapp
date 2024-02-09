from customer import Customer as C
import shelve

def newOrderID():
    with shelve.open('orderID') as db:
        if 'orderID' not in db:
            db['orderID'] = 0
        db['orderID'] += 1
        return db['orderID']

class CustomerOrder(C):
    def init(self, phoneNumber, stall, orderID, item, itemQuantity, price, total, remarks, status):
        super().__init__()
        self.__stall = stall
        self.__orderID = orderID
        self.__item = item
        self.__itemQuantity = itemQuantity
        #self.__ingredient = ingredient
        #self.__ingredientQuantity = ingredientQuantity
        self.__price = price
        self.__total = total
        self.__remarks = remarks
        self.__status = status


    def get_stall(self):
        return self.__stall
    
    def get_orderID(self):
        return self.__orderID
    
    def get_item(self):
        return self.__item
    
    def get_itemQuantity(self):
        return self.__itemQuantity
    
    def get_ingredient(self):
        return self.__ingredient
    
    def get_ingredientQuantity(self):
        return self.__ingredientQuantity
    
    def get_price(self):
        return self.__price
    
    def get_total(self):
        return self.__total
    
    def get_remarks(self):
        return self.__remarks
    
    def get_status(self):
        return self.__status
    
    
    def set_stall(self, stall):
        self.__stall = stall

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_item(self, item):
        self.__item = item

    def set_itemQuantity(self, itemQuantity):
        self.__itemQuantity = itemQuantity

    def set_ingredient(self, ingredient):
        self.__ingredient = ingredient

    def set_ingredientQuantity(self, ingredientQuantity):
        self.__ingredientQuantity = ingredientQuantity

    def set_price(self, price):
        self.__price = price

    def set_total(self, total):
        self.__total = total

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return f"orderID: {self.get_orderID()}, phoneNumber: {self.get_id()}, stall: {self.get_stall()}, item: {self.get_item()}, itemQuantity: {self.get_itemQuantity()}, price: {self.get_price()}, total: {self.get_total()}, remarks: {self.get_remarks()}, status: {self.get_status()}"