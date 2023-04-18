from blockchain import Blockchain

b = Blockchain()

b.add_node('127.0.0.1', 5000)
print(b.get_nodes())
