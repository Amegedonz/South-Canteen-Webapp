from customer import Customer as C

class CustomerLogin(C):
    def __init__(self, phoneNumber, password, rememberMe):
        super().__init__(phoneNumber, password)
        self.__rememberMe = rememberMe
        #check flask-login manager