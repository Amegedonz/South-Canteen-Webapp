from customer import Customer as C

class CustomerLogin(C):
    def __init__(self, phoneNumber, password, remeberMe):
        super().__init__(phoneNumber, password)
        self.__rememberMe = remeberMe

class RegisterCustomer(C):
    def __init__(self, name, phoneNumber, password, gender, membership):
        super().__init__(phoneNumber, password)
        self.set_name(name)
        self.set_gender(gender)
        self.set_membership(membership)

class DeleteCustomer(C):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber, password)






