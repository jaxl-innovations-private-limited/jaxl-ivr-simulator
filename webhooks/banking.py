import random

class account:
    def __init__(self,acc):
        self.accountN0=acc
        self.balance=random.randint(5000,80000)
    
    def transfer(self,to,ammount):
        if(ammount>self.balance):
            return "insufficient balance , transaction failed"
        self.balance-=ammount
        to.balance+=ammount
        return "transaction successfull now your balance is" +str(self.balance)
    def bal_enquiry(self):
        return "your balance is"+str(self.balance)
