import random
from . import MAIN_MENU_PROMPT,MAIN_MENU
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
    "exit",
    "askForExit"
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
        nextState=states[-1]
    elif data=="2":
        prompts=["enter account number of beneficiary and then ammount separated by # and ending with *"]
        chL="*"
        nextState=states[2]
    elif data=="3":
        prompts=['your last five transactions are']+acc.fiveTR()+ending
        chL=1
        nextState=states[-1]
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

def askForExit(data,acc):
    if(data=='*'):
        return [MAIN_MENU,menu]
    if data=='#':
        response=JaxlIVRResponse(
            prompt=["good by","have a good day"],
            num_characters=1,
            stream=None,
        )
        return [response,"exit"]


def tansferring_money(data:str,acc:account):
    try:
        beneficiary,ammount=data.split('#')
        if(len(beneficiary)!=6):
            raise ArithmeticError
        beneficiary=int(beneficiary)
        ammount=int(ammount[0:-1])
    except:
        response=JaxlIVRResponse(
            prompt=['Invalid Input',
                    "enter account number of beneficiary and then ammount separated by # and ending with *"],
            num_characters="*",
            stream=None,
        )
        return [response,states[2]]
    beneficiary=account(beneficiary)
    prompts=[acc.transfer(beneficiary,ammount)]+ending
    response=JaxlIVRResponse(
            prompt=prompts,
            num_characters=1,
            stream=None,
        )
    return [response,states[-1]]

def block_card(data,acc:account):
    try:
        card=int(data)
    except:
        response=JaxlIVRResponse(
            prompt=['Invalid Input',
                    'enter 16 digit car number'],
            num_characters=16,
            stream=None,
        )
        return [response,states[4]]
    #In future blocking card logic will be developed and added here
    #for now just let make it 
    response=JaxlIVRResponse(
            prompt=["your card has been successfully blocked"]+ending,
            num_characters=1,
            stream=None,
        )
    return [response,states[-1]]
