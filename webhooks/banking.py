import random
from . import MAIN_MENU_PROMPT
from jaxl.ivr.frontend.base import (
    # BaseJaxlIVRWebhook,
    # ConfigPathOrDict,
    # JaxlIVRRequest,
    JaxlIVRResponse,
)

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



states=[
    "menu",
    "balance",
    "transferring_money",
    "five_transactions ",
    "block_card",
    "exit"
]

ending=["enter * for main menu",
        "enter # to end this call"]


def menu(data,acc:account,):
    prompts=[]
    chL=0
    nextState=menu
    if data=="1":
        prompts=[acc.bal_enquiry()]+ending
        chL=6
        nextState=states[1]
    elif data=="2":
        prompts=["enter account number of beneficiary and then ammount separated by # and ending with *"]
        chL="*"
        nextState=states[2]
    elif data=="3":
        prompts=['your last five transactions are']+acc.fiveTR()
        chL=1
        nextState=states[3]
    elif data=="4":
        prompts=['enter 16 digit car number']
        chL=16
        nextState=states[4]
    elif data=='9':
        prompts=MAIN_MENU_PROMPT
        chL=1
        nextState=states[0]
    else :
        prompts=["Invalid input"]


    response=JaxlIVRResponse(
            prompt=prompts,
            num_characters=chL,
            stream=None,
        )
    return [response,nextState]

def balance(data,acc):

