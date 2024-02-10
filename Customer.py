#import User

class Customer():
    count_id = 0

    def __init__(self, food ,quantiy, remark, order_time):
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__food = food
        self.__quantity = quantiy
        self.__remark = remark
        self.__order_time = order_time


    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_food(self):
        return self.__food

    def get_quantity(self):
        return self.__quantity

    def get_remark(self):
        return self.__remark

    def get_order_time(self):
        return self.__order_time

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_food(self, food):
        self.__food = food

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_remark(self, remark):
        self.__remark = remark

    def set_order_time(self,order_time):
        self.__order_time = order_time
