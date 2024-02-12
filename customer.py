class Customer:
    def __init__(self, phoneNumber):
        self.__id =str(phoneNumber)

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

    def get_name(self):
        return self.__name
    
    def get_id(self):
        return str(self.__id)
    
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
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
    def __str__(self):
        return f"User {self.get_name()} with phone number {self.get_id()}"
    

