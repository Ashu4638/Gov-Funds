from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from . import blockchain
from . import transaction
from .Block import Block

fund = blockchain.Blockchain(10000, "Scholarship")
# fund.createTransaction(transaction.Transaction("Address1", "Address2", 100))
# fund.createTransaction(transaction.Transaction("Address2", "Address1", 50))
# fund.minependingTransacrions()
# fund.createTransaction(transaction.Transaction("Address1", "Address2", 100))
# fund.createTransaction(transaction.Transaction("Address2", "Address1", 50))
data = {"funds" : [fund]}



def index(request):


    return render(request, 'index.html', data)

def admin(request):
    if request.user.is_authenticated and request.user.username == "admin":
        return render(request,'admin.html' ,data)
    else:
        return render(request, 'login.html')


def loginform(request):
    if request.user.is_authenticated and request.user.username != "admin":
        return render(request, 'transaction.html', data)
    elif request.user.is_authenticated and request.user.username == "admin":
        return render(request,'admin.html' ,data)
    else:
        return render(request, 'login.html')

def createTransaction(request):
    if request.user.is_authenticated and request.user.username != "admin":
        if request.method == 'POST':
            fromAdd = request.POST.get('fundname')
            toAdd = request.user.username
            amount = int(request.POST['amount'])
            print(fromAdd)
            print(toAdd)
            fund = data["funds"][0]
            for ptr in range (0,len(data["funds"])):
                if data["funds"][ptr].name == fromAdd:
                    data["funds"][ptr].createTransaction(transaction.Transaction(fromAdd, toAdd, amount))
                    break
            return render(request,'transaction.html', data)
        else:
            return HttpResponse("404 - Not Allowed")
    else:
        return render(request, 'login.html')


def Mine(request):
    if request.user.is_authenticated and request.user.username == "admin":
        chain = data["funds"][0]
        name = ""
        if request.method == 'POST':
            name = request.POST.get('block')
            print(name)
            for ptr in range (0,len(data["funds"])):
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('block')
            print("print")
            print(name)
            fund = data["funds"][0]
            for ptr in range (0,len(data["funds"])):
                if data["funds"][ptr].name == name:
                    data["funds"][ptr].minependingTransacrions()
                    return render(request, 'blockchain.html', {"funds": data["funds"][ptr].chain, "name": data["funds"][ptr].name})
        return HttpResponse("failed")
    else:
        return render(request, 'login.html')
def viewblockchain(request):
    if request.method == 'POST':
        name = request.POST.get('block')
        fund = data["funds"][0]
        for ptr in range (0,len(data["funds"])):
            if data["funds"][ptr].name == name:
                return render(request, 'blockchain.html', {"funds": data["funds"][ptr].chain, "name" : data["funds"][ptr].name})
    return HttpResponse("Failed")
def viewtransaction(request):
    block = Block(timestamp="", transactions=[], prev="")
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

def addfund(request):
    if request.user.is_authenticated and request.user.username == "admin":
        return render(request, 'addFund.html')
    else:
        return render(request, 'login.html')

def appendfund(request):
    if request.user.is_authenticated and request.user.username == "admin":

        if request.method == 'POST':
            fundname = request.POST['fundname']
            amount = request.POST['amount']
            print(amount)
            print(fundname)
            temp = blockchain.Blockchain(int(amount), fundname)
            print(temp.chain)
            data["funds"].append(temp)
        return render(request, 'addFund.html')
    else:
        return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')


def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if(username == "admin"):
                login(request, user)
                return render(request, 'admin.html',data)
            else:
                login(request, user)
                messages.success(request, "Login Sucess")
                return render(request,'transaction.html', data)
    else:
        return HttpResponse("404 - Not Allowed")
    return HttpResponse("None")
def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'index.html',data)
def contact(request):
    return render(request, 'contact.html')
def register(request):
    return render(request, 'register.html')

def singup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['email']
        password = request.POST['pass']
        rpass = request.POST['rpass']


        myuser  = User.objects.create_user(name, username, password)
        myuser.save()
        messages.success(request, "Account Created")
        return redirect("/")
    else:
        return HttpResponse("404 - Not Allowed")
