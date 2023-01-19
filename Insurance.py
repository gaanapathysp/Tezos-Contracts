import smartpy as sp

class NFTInsurance(sp.Contract):
    def _init_(self):
        self.init(nft_collateral = sp.map(tkey = sp.TAddress, tvalue = sp.TInt))

    @sp.entry_point
    def deposit(self, params):
        sp.verify(sp.is_owner(params.sender))
        self.data.nft_collateral[params.nft_id] = params.value

    @sp.entry_point
    def withdraw(self, params):
        sp.verify(sp.is_owner(params.sender))
        sp.verify(self.data.nft_collateral.contains(params.nft_id))
        self.data.nft_collateral.remove(params.nft_id)

def test():
    scenario = sp.test_scenario()
    alice = scenario.accounts[0]
    bob = scenario.accounts[1]
    contract = NFTInsurance()
    scenario += contract
    scenario += contract.deposit(sender=alice, nft_id="123", value=100)
    scenario += contract.withdraw(sender=alice, nft_id="123")
    scenario.verify(contract.data.nft_collateral.size() == 0)