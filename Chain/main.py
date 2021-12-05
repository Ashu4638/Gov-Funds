from . import blockchain
from . import transaction
coin = blockchain.Blockchain()
def main():
    coin = blockchain.Blockchain()

    coin.createTransaction(transaction.Transaction("Address1", "Address2", 100))
    coin.createTransaction(transaction.Transaction("Address2", "Address1", 50))
    print("Starting Miner")
    coin.minependingTransacrions("Ashu-Wallet")
    Chain = []
    for block in coin.chain:
        Chain.append({"Prev" : block.prev, "Curr" : block.hash, "Nonce" : str(block.Nonce),"Time" : str(block.timestamp),"Valid" : coin.isChainValid(), "transactions" : block.transactions })

        print("Prev" + block.prev)
        print("Curr" + block.hash)
        print("NOnce" + str(block.Nonce))
        print("Time" + str(block.timestamp))
        for tran in block.transactions:
            print("From" + str(tran.fromAdd))
            print(tran.toAdd)
            print(tran.amount)


    print("Balace of Ashu = " + str(coin.getBalanceofAdd("Ashu-Wallet")))
    print(coin.isChainValid())

    return Chain, coin.pendingtransactions

main()