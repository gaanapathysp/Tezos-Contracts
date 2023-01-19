import smartpy as sp

class RealEstateNFT(sp.Contract):
    def _init_(self):
        self.init(nft_collateral = sp.map(tkey = sp.TAddress, tvalue = sp.TAddress),
                  properties = sp.map(tkey = sp.TAddress, tvalue = sp.TMap(tkey = sp.TStr, tvalue = sp.TInt)))

    @sp.entry_point
    def deposit_property(self, params):
        sp.verify(sp.is_owner(params.sender))
        self.data.properties[params.property_id] = params.property_data

    @sp.entry_point
    def deposit_nft(self, params):
        sp.verify(sp.is_owner(params.sender))
        sp.verify(self.data.properties.contains(params.property_id))
        self.data.nft_collateral[params.nft_id] = params.property_id

    @sp.entry_point
    def withdraw_nft(self, params):
        sp.verify(sp.is_owner(params.sender))
        sp.verify(self.data.nft_collateral.contains(params.nft_id))
        self.data.nft_collateral.remove(params.nft_id)
        
    @sp.entry_point
    def transfer_property(self,params):
        sp.verify(sp.is_owner(params.sender))
        sp.verify(self.data.nft_collateral.contains(params.nft_id))
        self.data.nft_collateral[params.nft_id] = params.new_owner

def test():
    scenario = sp.test_scenario()
    alice = scenario.accounts[0]
    bob = scenario.accounts[1]
    contract = RealEstateNFT()
    scenario += contract
    property_data = sp.map(name = "property_name", location = "property_location", value=100)
    scenario += contract.deposit_property(sender=alice, property_id="123", property_data=property_data)
    scenario += contract.deposit_nft(sender=alice, nft_id="456", property_id="123")
    scenario += contract.transfer_property(sender=alice,nft_id = "456", new_owner = bob)
    scenario.verify(contract.data.nft_collateral[sp.TAddress("456")] == bob)