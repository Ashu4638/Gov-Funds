from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from . import blockchain
from . import transaction
from .Block import Block
from .models import Wallets
from .models import History
from datetime import datetime
import pickle
fund = blockchain.Blockchain(10000, "Scholarship")
# fund.createTransaction(transaction.Transaction("Address1", "Address2", 100))
# fund.createTransaction(transaction.Transaction("Address2", "Address1", 50))
# fund.minependingTransacrions()
# fund.createTransaction(transaction.Transaction("Address1", "Address2", 100))
# fund.createTransaction(transaction.Transaction("Address2", "Address1", 50))
data = {"funds":[]}
def load_data():
    with open("blockchain.pkl", "rb") as file:
        data = pickle.load(file)

load_data()

def index(request):
    load_data()
    return render(request, 'index.html', data)

def admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'admin.html' ,data)
    else:
        return render(request, 'login.html')


def loginform(request):
    load_data()
    if request.user.is_authenticated and not request.user.is_staff:
        return render(request, 'transaction.html', data)
    elif request.user.is_authenticated and request.user.is_staff:
        return render(request,'admin.html' ,data)
    else:
        return render(request, 'login.html')

def createTransaction(request):
    load_data()
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == 'POST':
            fromAdd = request.POST.get('fundname')
            toAdd = request.user.username
            amount = int(request.POST['amount'])
            print(fromAdd)
            print(toAdd)
            # fund = data["funds"][0]

            for ptr in range (0,len(data["funds"])):
                if data["funds"][ptr].name == fromAdd:
                    data["funds"][ptr].createTransaction(transaction.Transaction(fromAdd, toAdd, amount))
                    History(fromAdd=fromAdd, toAdd=toAdd, amount=amount, timestamp=datetime.now(), status="Requested").save()
                    print("Transaction Added")
                    print(data["funds"][ptr].name)
                    with open("blockchain.pkl", "wb") as file:
                        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                    break
            return render(request,'transaction.html', data)
        else:
            return HttpResponse("404 - Not Allowed")
    else:
        return render(request, 'login.html')


def Mine(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        chain = data["funds"][0]
        name = ""
        if request.method == 'POST':
            name = request.POST.get('block')
            print(name)
            for ptr in range (0,len(data["funds"])):
                print(data["funds"][ptr].name)
                print(data["funds"])
                if data["funds"][ptr].name == name:
                    chain = data["funds"][ptr]
                    break
            print(chain.pendingtransactions)
        if len(chain.pendingtransactions) == 0:

            messages.error(request, "No Transactions")
            return render(request, 'admin.html', data)
        else:
            return render(request, 'Mine.html', {"transactions":chain.pendingtransactions, "name" : name})
    else:
        return render(request, 'login.html')

def addblock(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            name = request.POST.get('block')
            print("print")
            print(name)
            fund = data["funds"][0]
            for ptr in range (0,len(data["funds"])):
                if data["funds"][ptr].name == name:
                    for trans in data["funds"][ptr].pendingtransactions:
                        user_wallets = Wallets.objects.filter(username= trans.toAdd)
                        for wallet in user_wallets:
                            wallet.balance += trans.amount
                            print(wallet.balance)
                            print(trans.amount)
                            Wallets.objects.filter(username=trans.toAdd).update(balance = wallet.balance)
                        History.objects.filter(timestamp= trans.timestamp, toAdd=trans.toAdd).update(status="Approved")


                    data["funds"][ptr].minependingTransacrions()
                    with open("blockchain.pkl", "wb") as file:
                        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                    return render(request, 'blockchain.html', {"funds": data["funds"][ptr].chain, "name": data["funds"][ptr].name})
        return HttpResponse("failed")
    else:
        return render(request, 'login.html')
def viewblockchain(request):
    load_data()
    if request.method == 'POST':
        name = request.POST.get('block')
        print(name)
        for ptr in range (0,len(data["funds"])):
            if data["funds"][ptr].name == name:
                return render(request, 'blockchain.html', {"funds": data["funds"][ptr].chain, "name" : data["funds"][ptr].name})
    return HttpResponse("Failed")
def viewtransaction(request):
    load_data()
    if request.method == 'POST':
        name = request.POST.get('fund')
        hash = request.POST.get('hash')
        print("begin")
        print(name)
        print(hash)
        for ptr in range (0,len(data["funds"])):
            if data["funds"][ptr].name == name:
                for i in range (0,len(data["funds"][ptr].chain)):
                    print(data["funds"][ptr].chain[i].hash)
                    if data["funds"][ptr].chain[i].hash == hash:
                        return render(request, 'viewtransaction.html', {"transactions": data["funds"][ptr].chain[i].transactions})
                        break
    return HttpResponse("Failed")
def wallet(request):
    load_data()
    if request.user.is_authenticated and not request.user.is_staff:
        my_wallets = Wallets.objects.filter(username = request.user)
        my_trans = History.objects.filter(toAdd=request.user).order_by('-timestamp')
        return render(request, "wallet.html",{"wallets" : my_wallets, "Transactions":my_trans})
    else:
        return render(request, "login.html")
def addfund(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'addFund.html')
    else:
        return render(request, 'login.html')

def appendfund(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:

        if request.method == 'POST':
            fundname = request.POST['fundname']
            if " " in fundname:
                messages.error(request, "Space is Not Allwed in Fund Name !")
                return render(request, 'addFund.html')
            for fund in data["funds"]:
                if fund.name == fundname:
                    messages.error(request, "Fund Alredy Exists !")
                    return render(request, 'addFund.html')
            amount = request.POST['amount']
            print(amount)
            print(fundname)
            # temp = blockchain.Blockchain(int(amount), fundname)
            # print(temp.chain)

            data["funds"].append(blockchain.Blockchain(int(amount), fundname))
            with open("blockchain.pkl", "wb") as file:
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            messages.success(request, "Fund Added Successfully !")

        return render(request, 'addFund.html')
    else:
        return render(request, 'login.html')


def deleteTransaction(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            name = request.POST['fund']
            hash = request.POST['hash']
            print(name)
            print(hash)
            for ptr in range (0,len(data["funds"])):
                print(data["funds"][ptr].name )
                if data["funds"][ptr].name == name:
                    for i in range (0, len(data["funds"][ptr].pendingtransactions)):
                        if data["funds"][ptr].pendingtransactions[i].hash == hash:
                            History.objects.filter(timestamp=data["funds"][ptr].pendingtransactions[i].timestamp, toAdd=data["funds"][ptr].pendingtransactions[i].toAdd).update(
                                status="Rejected")
                            data["funds"][ptr].pendingtransactions.pop(i)
                            with open("blockchain.pkl", "wb") as file:
                                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                            return render(request, 'Mine.html', {"transactions":data["funds"][ptr].pendingtransactions, "name" : name})

            return HttpResponse("404 Error Not Found")
    else:
        return render(request,"login.html")



def about(request):
    return render(request, 'about.html')


def handlelogin(request):
    load_data()
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if(user.is_staff):
                login(request, user)
                messages.success(request, "Login Sucess")
                return render(request, 'admin.html',data)
            else:
                login(request, user)
                messages.success(request, "Login Sucess")
                return render(request,'transaction.html', data)


    else:
        return HttpResponse("404 - Not Allowed")

def editfund(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "editfund.html", data)
    else:
        return render(request, "login.html")
def deletefund(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        name  = request.POST['fund']
        print(name)
        for ptr in range(len(data["funds"])):
            if data["funds"][ptr].name == name:
                data["funds"].pop(ptr)
                with open("blockchain.pkl", "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                return render(request, "editfund.html", data)
    else:
        return render(request, "login.html")

def updatefund(request):
    load_data()
    if request.user.is_authenticated and request.user.is_staff:
        name = request.POST['fund']
        amount = int(request.POST['amount'])
        for ptr in range(len(data["funds"])):
            if data["funds"][ptr].name == name:
                data["funds"][ptr].fund = amount
                with open("blockchain.pkl", "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                return render(request, "editfund.html", data)
        return HttpResponse("Failed")
    else:
        return render(request, "login.html")

def handlelogout(request):
    load_data()
    if request.method == 'POST':
        logout(request)
        return render(request, 'index.html',data)
def contact(request):
    return render(request, 'contact.html')
def register(request):
    return render(request, 'register.html')

def singup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['email']
        password = request.POST['pass']
        rpass = request.POST['rpass']
        if password != rpass:
            messages.error(request,"Password doesn't match")
            return render(request, "register.html")
        print(User.objects.all())
        for name in User.objects.all():
            if name.username == username:
                messages.error(request, "Email Already Exists !")
                return render(request, "register.html")
        myuser  = User.objects.create_user(username=username, password=password, email=username)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        Wallets(username=username, balance=0).save()
        messages.success(request, "Account Created")
        return redirect("/")
    else:
        return HttpResponse("404 - Not Allowed")
