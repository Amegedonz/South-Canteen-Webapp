from store_owner import StoreOwner as S

class StoreOwnerLogin(S):
    def __init__(self, phoneNumber, password):
        self.set_phoneNumber = phoneNumber
        self.set_password = password

class CreateStoreOwner(S):
    def __init__(self, storeId, phoneNumber, password):
        self.set_storeId = storeId
        self.set_phoneNumber = phoneNumber
        self.set_password = password



storeOwners = {
    1 : CreateStoreOwner(1, "90000001", "Store1")
}