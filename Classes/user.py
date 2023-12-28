class User:
    count_id = 0
    def __init__(self, user_id, first_name, last_name, gender):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender

    def get_cust_id(self):
        return self.__user_id
    
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_gender(self):
        return self.__gender
    
    def set_cust_id(self, user_id):
        self.__user_id = User.count_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender
