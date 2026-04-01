from web3 import Web3
import json

class Web3Client:

    def __init__(self, rpc_url, contract_address, abi_path):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        with open(abi_path) as f:
            abi = json.load(f)

        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

    def registrar_idea(self, private_key, idea_id, refs):
        account = self.w3.eth.account.from_key(private_key)

        tx = self.contract.functions.registrar(
            idea_id,
            refs
        ).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('20', 'gwei')
        })

        signed = account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)

        return tx_hash.hex()
