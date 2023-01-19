import smartpy as sp

class NFT(sp.Contract):
    def _init_(self):
        self.init(token_id = sp.map(tkey = sp.TAddress, value = sp.TInt))
        
    @sp.entry_point
    def mint(self, params):
        token_id = sp.rand_bytes(32)
        self.data.token_id[token_id] = params.value
        sp.transfer(params.to, params.value)

    @sp.entry_point
    def transfer(self, params):
        sp.require(self.data.token_id.contains(params.token_id))
        sp.transfer(params.to, self.data.token_id[params.token_id])
        del self.data.token_id[params.token_id]

def test():
    c1 = sp.test_account("c1")
    c2 = sp.test_account("c2")
    c3 = sp.test_account("c3")
    scenario = sp.test_scenario()
    scenario.h1("Minting and Transferring NFTs")
    scenario += c1.transfer(sp.tez(1000000))
    scenario += NFT()
    scenario += NFT.mint(token_id = sp.rand_bytes(32), to = c2, value = sp.tez(100))
    scenario += NFT.transfer(token_id = sp.rand_bytes(32), to = c3, value = sp.tez(100))

test()