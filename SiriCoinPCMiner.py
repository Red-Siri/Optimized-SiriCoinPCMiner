import time, json, sha3, sys, os, termcolor, requests, cpuinfo
from web3.auto import w3
from eth_account.messages import encode_defunct


MainNET = "https://node-1.siricoin.tech:5006"
ShreyasNET = "http://138.197.181.206:5005"
JunaidNET = 'http://47.250.59.81:5005'

TimeOUT = 1

if os.name == 'nt': os.system('color')


def Get_address():
    global address_valid, minerAddr
    while not address_valid:
        minerAddr = input(termcolor.colored("Enter your SiriCoin address: ", 'magenta'))
        try:
            address_valid = w3.isAddress(minerAddr)
        except:
            print(termcolor.colored("The address you inputed is invalid, please try again", "red"))
        if not address_valid:
            print(termcolor.colored("The address you inputed is invalid, please try again", "red"))
    

class SignatureManager(object):
    def __init__(self):
        self.verified = 0
        self.signed = 0
    
    def signTransaction(self, private_key, transaction):
        message = encode_defunct(text=transaction["data"])
        transaction["hash"] = w3.soliditySha3(["string"], [transaction["data"]]).hex()
        _signature = w3.eth.account.sign_message(message, private_key=private_key).signature.hex()
        signer = w3.eth.account.recover_message(message, signature=_signature)
        sender = w3.toChecksumAddress(json.loads(transaction["data"])["from"])
        if (signer == sender):
            transaction["sig"] = _signature
            self.signed += 1
        return transaction

class SiriCoinMiner(object):
    def __init__(self, NodeAddr, RewardsRecipient):
        self.node = NodeAddr
        self.signer = SignatureManager()
        self.difficulty = 1
        self.target = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        self.lastBlock = ""
        self.rewardsRecipient = w3.toChecksumAddress(RewardsRecipient)
        self.priv_key = w3.solidityKeccak(["string", "address"], ["SiriCoin Will go to M00N - Just a disposable key", self.rewardsRecipient])

        self.nonce = 0
        self.acct = w3.eth.account.from_key(self.priv_key)
        self.messages = b"null"
        
        self.timestamp = time.time()
        _txs = requests.get(f"{self.node}/accounts/accountInfo/{self.acct.address}").json().get("result").get("transactions")
        self.lastSentTx = _txs[len(_txs)-1]
        self.refresh()
    
    def refresh(self):
        info = requests.get(f"{self.node}/chain/miningInfo").json().get("result")
        self.target = info["target"]
        self.difficulty = info["difficulty"]
        self.lastBlock = info["lastBlockHash"]
        _txs = requests.get(f"{self.node}/accounts/accountInfo/{self.acct.address}").json().get("result").get("transactions")
        self.lastSentTx = _txs[len(_txs)-1]
        self.timestamp = time.time()
        self.nonce = 0
    
    def submitBlock(self, blockData):
        tx = self.signer.signTransaction(self.priv_key, {"data": json.dumps({"from": self.acct.address, "to": self.acct.address, "tokens": 0, "parent": self.lastSentTx, "blockData": blockData, "epoch": self.lastBlock, "type": 1})})
        self.refresh()
        try:
            txid = requests.get(f"{self.node}/send/rawtransaction/?tx={json.dumps(tx).encode().hex()}").json().get("result")[0]
            print(termcolor.colored(f"Mined block {blockData['miningData']['proof']},\nsubmitted in transaction {txid}", "green"))
            print(termcolor.colored("Current Network Balance : " + str(requests.get(f"{self.node}/accounts/accountBalance/{self.rewardsRecipient}").json()["result"]["balance"]) + " Siri", "green")) # code by luketherock868
            miner.startMining()
        except:
            print(termcolor.colored("Oops, failed subminting the block, wait till mainnet is back up and enter in this URL in your browser, ignore the output, just do it ;D \n", "red"))
            print(termcolor.colored(str(f"https://siricoin-node-1.dynamic-dns.net:5005/send/rawtransaction/?tx={json.dumps(tx).encode().hex()}", "cyan")))
            sys.exit()
            




    def beaconRoot(self):
        messagesHash = sha3.keccak_256(self.messages).digest()
        bRoot = "0x" + sha3.keccak_256((b"".join([bytes.fromhex(self.lastBlock.replace("0x", "")), int(self.timestamp).to_bytes(32, 'big'), messagesHash, bytes.fromhex(self.rewardsRecipient.replace("0x", "")) ]))).hexdigest() # parent PoW hash (bytes32), beacon's timestamp (uint256), hash of messages (bytes32), beacon miner (address)
        return bRoot

    def proofOfWork(self, bRoot, nonce):
        proof = sha3.keccak_256((b"".join([bytes.fromhex(bRoot.replace("0x", "")),nonce.to_bytes(32, 'big')]))).hexdigest()
        return "0x" + proof

    def formatHashrate(self, hashrate):
        if hashrate < 1000:
            # H's
            if len(str(round(hashrate, 2)).split('.', 1)[1]) == 1: return str(round(hashrate/1000, 2)) + "0 H/s" 
            else: return str(round(hashrate/1000, 2)) + " H/s"
        elif hashrate < 1000000:
            # KH's
            if len(str(round(hashrate/1000, 2)).split('.', 1)[1]) == 1: return str(round(hashrate/1000, 2)) + "0 KH/s" 
            else: return str(round(hashrate/1000, 2)) + " KH/s"
        elif hashrate < 1000000000:
            # MH's
            if len(str(round(hashrate/1000000, 2)).split('.', 1)[1]) == 1: return str(round(hashrate/1000, 2)) + "0 MH/s" 
            else: return str(round(hashrate/1000, 2)) + " MH/s"
        elif hashrate < 1000000000000:
            # GH's
            if len(str(round(hashrate/1000000000, 2)).split('.', 1)[1]) == 1: return str(round(hashrate/1000, 2)) + "0 GH/s" 
            else: return str(round(hashrate/1000, 2)) + " GH/s"
        
            
            
    def startMining(self):
        self.refresh()
        global first_run, bRoot
        if first_run: print(termcolor.colored(f"Started mining for {self.rewardsRecipient} on {the_node}", "yellow"))
        proof = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        while True:
            self.refresh()
            bRoot = self.beaconRoot()
            first_run = False
            while (time.time() - self.timestamp) < 30:
                self.nonce += 1
                proof = self.proofOfWork(bRoot, self.nonce)
                if (int(proof, 16) < int(self.target, 16)):
                    rawTX = ({"miningData" : {"miner": self.rewardsRecipient,"nonce": self.nonce,"difficulty": self.difficulty,"miningTarget": self.target,"proof": proof}, "parent": self.lastBlock,"messages": self.messages.hex(), "timestamp": int(self.timestamp), "son": "0000000000000000000000000000000000000000000000000000000000000000"})
                    self.submitBlock(rawTX)
            print(termcolor.colored("Last 30 seconds hashrate: " + self.formatHashrate((self.nonce / 30)), "yellow"))


if __name__ == "__main__":
    first_run = True
    address_valid = False
    
    
    print(termcolor.colored("---------------------------- System ----------------------------", "yellow"))
    print(termcolor.colored("OS: " + platform.system() + " " + platform.release(), "yellow"))
    print(termcolor.colored("CPU: " + cpuinfo.get_cpu_info()['brand_raw'] +" @ "+ cpuinfo.get_cpu_info()['hz_advertised_friendly'] + " (x"+str(cpuinfo.get_cpu_info()['count'])+")", "yellow"))
    print(termcolor.colored("RAM: " + str(round(int(psutil.virtual_memory()[3]) / 1074000000, 2)) + " / " + str(round(float(psutil.virtual_memory()[0]) / 1074000000, 2)) + " GB", "yellow"))
    print(termcolor.colored("----------------------------------------------------------------", "yellow")) # code by luketherock868
    
    Get_address()
        
    try:
        if requests.get(f"{MainNET}/chain/block/2", timeout=TimeOUT).json()["result"]["height"] == 2:
            the_node = "main-net"
            miner = SiriCoinMiner(MainNET, minerAddr)
            Continue_To_Shreyas_net = False
            miner.startMining()
    except requests.ConnectTimeout:
        Continue_To_Shreyas_net = True
    
    try:
        if Continue_To_Shreyas_net and requests.get(f"{ShreyasNET}/chain/block/1", timeout=TimeOUT).json()["result"]["height"] == 1:
            Continue_To_Junaid_net = False
            print(termcolor.colored("Whoops! The main-net is offline, you can try mining on the Shreyas-net, but it's not recommended as it's not designed to mine, if you hit a block the balance won't move over to main-net.", "red"))
            on_ShreyasNET = input(termcolor.colored("Are you sure you wan't to continue? Y/n \n", "magenta"))
            if on_ShreyasNET.lower() == "y":
                the_node = "Shreyas-net"
                miner = SiriCoinMiner(ShreyasNET, minerAddr)
                miner.startMining()
            if on_ShreyasNET.lower() == "n":
                print(termcolor.colored("Ok, quitting the miner, goodbye!", "red"))
                sys.exit()
            
    except requests.ConnectTimeout:

        Continue_To_Junaid_net = True

    try:
        if Continue_To_Junaid_net and requests.get(f"{JunaidNET}/chain/block/1", timeout=TimeOUT).json()["result"]["height"] == 1:
            the_node = "Junaid-net"
            miner = SiriCoinMiner(JunaidNET, minerAddr)
            Continue_To_main_net = False
            miner.startMining()
    except requests.ConnectTimeout:
        print(termcolor.colored("All networks are down, quitting the miner, goodbye!", "red"))
        sys.exit()
        
