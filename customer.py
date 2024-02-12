#import User

class Customer():
    def __init__(self, phoneNumber):
        self.__phoneNumber = str(phoneNumber)

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
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return str(self.__phoneNumber)
    
    def get_password(self):
        return self.__password
    
    def get_gender(self):
        return self.__gender
    
    def get_membership(self):
        return self.__membership
    
    def get_securityQuestion(self):
        return self.__securityQuestion
    
    def get_securityAnswer(self):
        return self.__securityAnswer

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

    def set_name(self, name):
        self.__name = name

    def set_id(self, phoneNumber):
        self.__id = phoneNumber

    def set_password(self, password):
        self.__password = password

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_securityQuestion(self, securityQuestion):
        self.__securityQuestion = securityQuestion

    def set_securityAnswer(self, securityAnswer):
        self.__securityAnswer = securityAnswer    

#Login requirements
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
#__str__ function
    def __str__(self):
        return f"User {self.get_name()} with phone number {self.get_id()}"