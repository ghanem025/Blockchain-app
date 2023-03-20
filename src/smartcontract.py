
# this is a list of all the doctors that can view the patients data
# This list will be encrypted using the patients public key
# and then to view it you need to decrypt it using the private
# so the contract holder (patient) would provide this data to the contract
# each time a contract is used, the smart contract would need this data to verify if a doctor is allowed to view the patients data.
auth_doctors = dict{'Name':"Dr. Balls", 'address': 'publickey'}


# So this will be a program that checks if the a doctor is allowed to view or change your medical history
# change in this case would be adding a new block to the chain with the patients updated data
# so the process is going to be like this
# doctor requests access to patients data (we should have a seperate page for the doctor to view data)
# now the smart contract will check if that doctor is verified to look at the patients data
# it will do this by looking at the authorized list, which it needs to use the patients private key to decrypt 
# once thats decrypted it checks if the requested doctor is on the list
# if they are we decrypt the data and allow him to view it or add a block if they choose to
# otherwise we refuse the transaction (this can be done by putting it inside an unconfirmed transaction list)
# and the whole process is closed


# here is how this is going to be done
# a doctor will send a signature (using there private key), the only way this signature can be read is by using the doctors public key
# this public key should already be given by the contract holder (patient), now the smart contract will check if this doctor is the real deal
# if the signature checks out, then we continue the authorization process. Now we use the patients private key to decrypt the data and allow the 
# doctor to view this data
class SmartContract:
    def authorized(transaction):
        if doctor in auth_doctors:
            #do stuff
    
    def check_signature():
        # check the auth_doctor dict and see if they are there
        # if they are not the contract will refuse the transaction.
        # otherwise we continue
        # 