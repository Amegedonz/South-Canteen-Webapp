from customer import Customer as C

class CustomerOrder(C):
    def init(self, phoneNumber, stall, orderID, item, quantity, price, total, remarks, status):
        super().init(phoneNumber)
        self.__stall = stall
        self.__orderID = orderID
        self.__item = item
        self.__quantity = quantity
        self.__price = price
        self.__total = total
        self.__remarks = remarks
        self.__status = status

    def set_stall(self, stall):
        self.__stall = stall    

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_item(self, item):
        self.__item = item

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_total(self, total):
        self.__total = total

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_status(self, status):
        self.__status = status

    def get_stall(self):
        return self.__stall
    
    def get_orderID(self):
        return self.__orderID
    
    def get_item(self):
        return self.__item
    
    def get_quantity(self):
        return self.__quantity
    
    def get_total(self):
        return self.__total
    
    def get_remarks(self):
        return self.__remarks
    
    def get_status(self):
        return self.__status