from user import *

class Customer(User):
    count_id = 0
    def __init__(self, cust_id, first_name, last_name, gender):
        super().__init__(first_name, last_name, gender)
        Customer.count_id += 1
        self.__cust_id = Customer.count_id

    def get_cust_id(self):
        return self.__cust_id
    
    def set_cust_id(self, cust_id):
        self.__cust_id = Customer.count_id

class CustomerLogin(Customer):
    def __init__(self, cust_id, first_name, last_name, gender, email, date_joined, address):
        super().__init__(cust_id, first_name, last_name, gender)
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
    
    def get_email(self):
        return self.__email
    
    def get_date_joined(self):
        return self.__date_joined
    
    def get_address(self):
        return self.__address

    def set_email(self, email):
        self.__email = email
    
    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_address(self, address):
        self.__address = address

class OrderedFood(Customer):
    def __init__(self, cust_id, stall_id, item_id, ):
        ...
