# Creating a Blockchain 
# Author: Nathaniel Pines

# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https:www.getpostman.com/

#imports 
import datetime #each block sill have its own time stamp
import hashlib #used to hash each block
import json #used to encode the blocks before being hashed 
from flask import Flask,jsonify #we will create an object of the Flask class and jsonify will be used to display requests via Postman 

#Building a Blockchain (architecture)
#when we work with a class we alsways start with the init method always takes one argument "self" 
class Blockchain:
    def __init__(self):
        self.chain = [] #initializing the chain of blocks 
        self.create_block(proof = 1, previous_hash = '0') #create the genesis block, using arbitrary values 
        
    def create_block(self, proof, previous_hash): #creates a block and adds it to the block chain 
        block = {'index': len(self.chain) + 1, #define the new block that has just been mined 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash} 
        self.chain.append(block)
        return block
    
    def get_previous_block(self): #how to get the previous block 
        return self.chain[-1]
        
    def proof_of_work(self, previous_proof): #how to get proof of work 
        new_proof = 1 #to get new proof, incriment by 1 at each iteration of a while loop until we get the right proof 
        check_proof = False
        while check_proof is False: #return 64 string (hexadecimal), start with leading zeros 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': #if first 4 values of hash are leading zeros then the miner approves the block, finds the new proof 
                check_proof = True
            else:
                new_proof += 1 #try with the next proof to see if it starts with 4 leading zeros 
        return new_proof
    
    def hash(self, block): #return the hash of the block
        encoded_block = json.dumps(block, sort_keys= True).encode() #encode the block so it can be accepeted by the sha256 function
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain): #checking if the chain is valid
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] #current block
            if block['previous_hash'] != self.hash(previous_block): #if previous block hash does not match
                return False
            previous_proof = previous_block['proof'] #proof of previous block 
            proof = block['proof'] #proof of current block 
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() #check if hash operation starts with 4 leading zeros
            if hash_operation[:4] != '0000':
                return False
            previous_block = block #previous block has to turn into current block 
            block_index += 1 #update incrementating variable
        return True 
    
#Mining a Blockchain
    
# Create a Web App to interact with the Blockchain
        
app = Flask(__name__) #instance of Flask class to make Web App

# Creating a Blockchain
     
blockchain = Blockchain() #instance of blockchain class

# Mining a new block 

@app.route('/mine_block', methods = ['GET']) #address that will trigger/ call the mine block function
def mine_block(): #mine block function
    previous_block = blockchain.get_previous_block() #need to get proof, need previous proof first, within the dictionary keys of previous block
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof) #call proof of work function 
    previous_hash = blockchain.hash(previous_block) #previous hash obtained by using the hash method in order to append block to chain 
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Congratulations, you mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']} #new dictionary to be displayed when block is mined 
    return jsonify(response), 200

# Getting the full blockchain
    
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)} #what will display when we do the GET request
    return jsonify(response), 200

# Checking if the blockchain is valid 
    
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'The Blockchain is valid!'}
    else:
        response = {'message' : 'The Blockchain is not valid!'}
    return jsonify(response), 200

# Running the App

app.run(host = '0.0.0.0', port = 5000)
    
    
