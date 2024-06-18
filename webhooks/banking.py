import random



#may be implementend in future but till now only based on random numbers

class account:
    def __init__(self,acc):
        self.accountN0=acc
        self.balance=random.randint(5000,80000)
        self.transactions=[]
        while len(self.transactions)<5:
            ammount=random.randint(-5000,5000)
            if ammount==0:
                continue
            self.transactions.append([ammount,random.randint(111111,999999)])
    
    def transfer(self,to,ammount):
        if(ammount>self.balance):
            return "insufficient balance , transaction failed"
        self.balance-=ammount
        to.balance+=ammount
        self.transactions.append([ammount,to])
        return "transaction successfull now your balance is" +str(self.balance)
    
    def bal_enquiry(self):
        return "your balance is"+str(self.balance)
    
    def fiveTR(self):
        lst=[]
        for i in self.transactions:
            if i[0]<0:
                tr="debit to"
            else :
                tr="credit from"
            lst.append(tr+" account "+i[1])
        return lst

def getAcc(phone):
    acc=random.randint(111111,999999)
    return account(acc)


