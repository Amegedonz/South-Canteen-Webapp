class StoreOwner:
    def __init__(self):
        None

    def set_storeId(self, storeId):
        self.__storeId = storeId

    def set_phoneNumber(self, phoneNumber):
        self.__phoneNumber = phoneNumber

    def set_password(self, password):
        self.__password = password

    def get_storeId(self):
        return self.__storeId
    
    def get_phoneNumber(self):
        return self.__phoneNumber
    
    def get_password(self):
        return self.__password


