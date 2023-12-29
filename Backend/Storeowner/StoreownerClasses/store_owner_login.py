from store_owner import StoreOwner as S

class StoreOwnerLogin(S):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber, password)