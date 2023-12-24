class Customer:
    def __init__(self, name, phoneNumber, password):
        self.__name = name
        self.__phoneNumer = phoneNumber
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_phoneNumber(self, phoneNumber):
        self.__phoneNumer = phoneNumber

    def set_password(self, password):
        self.__password = password

    def get_name(self):
        return self.__name
    
    def get_phoneNumber(self):
        return self.__phoneNumer
    
    def get_password(self):
        return self.__password


class CustomerLogin(Customer):
    def __init__(self, phoneNumber, password, rememberMe):
        super().__init__(phoneNumber, password)
        self.__rememberMe = rememberMe
        #check flask-login manager


class OrderedFood(Customer):
    def __init__(self):
        ...
