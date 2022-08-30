import cryptocompare as cc
import json
from urllib.parse import urlparse
import requests
from datetime import date


class record:
    def __init__(self, name, buy, sell):
        self.buy = buy
        self.sell = sell
        self.name = name

    def __str__(self):
        print(self.name)
        print(self.sell)

    def recordData(self, profit):
        file1 = open('profits.txt', 'a')
        today = date.today()
        d1 = today.strftime("%m/%d/%y")
        file1.write(f"\n{d1} - {self.name}: {profit}")


def royaltyFees(collection):

    u = urlparse(collection)  # parses the url
    name = u.path  # gets the url path of what was inputed
    url = f"https://api.opensea.io/api/v1{name}"

    r = requests.get(url)  # requests data from the api

    packages_json = r.json()  # gets the json files from the requested api
    royalties_json = packages_json['collection'][
        'primary_asset_contracts']  # narrows down the data in the json file to a specific dictionary that contains the royalty fee (is a dictionary)

    packages_str = json.dumps(royalties_json)  # dumps json object into an element
    resp = json.loads(packages_str)  # load json into a string

    totalRoyalty = resp[0]['seller_fee_basis_points']  # gets the total royalty
    percentage = totalRoyalty / 10000
    return percentage


def option1():
    name = input("Project Name: ")
    collection = input("Project URL: ")
    buyPrice = float(input("Buy Price + Gas: "))
    sellPrice = float(input("Sell Price: "))
    totalRoyalty = royaltyFees(collection)
    totalSellPrice = sellPrice - (sellPrice * totalRoyalty)  # how much you actually got back accounting for fees
    profit = round((totalSellPrice - buyPrice), 4)  # amount made/lost
    listNFT = record(name, buyPrice, totalSellPrice)
    listNFT.recordData(profit)

    print(f"Profit made in ETH: {profit}")
    ethToUSD = cc.get_price('ETH', currency='USD')  # gets current price of etherium
    temp = ethToUSD.values()  # gets a dictionary of eth in USD
    v = str(*temp)  # removes dict_values and turns it into a string
    temp = v.split(":")  # splits the string into 2 parts (1st part 'USD', 2nd part price of eth)
    temp2 = temp[1]  # puts the 2nd part (price of eth) into temp 2
    temp3 = temp2[:-1]  # removes the hanging } at the end
    USD = float(temp3[1:])  # removes the space in the beginning
    price = profit * USD
    print(f"Profit made in USD: {price}")


def option2():
    collection = input("Please type the URL of the collection: ")
    buyPrice = float(input("Buy Price + Gas: "))
    totalRoyalty = royaltyFees(collection)
    print(totalRoyalty)
    breakEven = round((buyPrice + (buyPrice * totalRoyalty)), 4)
    print(f"You'll break even at {breakEven} ETH ")


def option3():
    file1 = open("profits.txt")
    numbers = file1.read()
    splitNum = numbers.split("\n")  # splits the file every time it ends a line (makes it a list)
    queue = []
    for i in range(len(splitNum)):
        queue.append(splitNum[i].split(":"))    #splits the list at the : so it seperates the number value

    str(queue)
    addedETH = 0
    for i in range(len(queue)):
        addedETH += float(queue[i][1])    #gets the number value

    print(f"Total Profit in Etherium: {round(addedETH, 4)}")
    ethToUSD = cc.get_price('ETH', currency='USD')  # gets current price of etherium
    temp = ethToUSD.values()  # gets a dictionary of eth in USD
    v = str(*temp)  # removes dict_values and turns it into a string
    temp = v.split(":")  # splits the string into 2 parts (1st part 'USD', 2nd part price of eth)
    temp2 = temp[1]  # puts the 2nd part (price of eth) into temp 2
    temp3 = temp2[:-1]  # removes the hanging } at the end
    USD = float(temp3[1:])  # removes the space in the beginning
    profitUSD = round((addedETH * USD), 2)
    print(f"Total Profit in USD: ${profitUSD}")

def option4():
    f = open('profits.txt', 'r')
    print(f.read())





print("Welcome to my Program. Please choose one of the following: ")
print("1) Record Profit")
print("2) How much to break even")
print("3) Profit List")
print("4) Raw Data")
print("5) Etherium to USD")
option = input("Please select an option: ")
if option == "1":
    option1()
elif option == "2":
    option2()
elif option == "3":
    option3()
elif option == "4":
    option4()
3