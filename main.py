# program for managing stock
# data structure for stock.txt {ItemID:[Name,Price,Units]}
# data structure for out of stock.txt {ItemID:Name}
# data structure for sales.txt {ItemID:[Name,Price,Units,Amount]}

"""
choices:
1)Sale
2)Add Items
3)Update Stock
4)View Stock
5)Total Sales
6)Restock Ledger
7)End
"""
import json

stock = 'stock.txt'
sales = 'sales.txt'
out_of_stock = 'out of stock.txt'
bill = 'bill.txt'

# string limiters

idlen = 4
qtylen = 5
numberlen = 8
namelen = 15


# function to convert the text file and convert to it's corresponding data type
def Scan(file):
    f = open(file, 'r')
    data = f.read()
    datadict = eval(data)
    f.close()
    return datadict


# function to update a particular text file with a dictionary
def Update(data, file, add=False, indices=[]):
    old_data = Scan(file)
    if not add:
        old_data.update(data)
    elif add:
        for i in data:
            if i in old_data:
                for j in indices:
                    old_data[i][j] += data[i][j]
            else:
                old_data[i] = data[i]
    f = open(file, 'w')
    f.write(json.dumps(old_data))
    f.close()


# function to add items to a text file in the form of a dictionary
def AddItems():
    data = {}
    cont = True
    while cont:
        odata = Scan(stock)
        item_id = input('Enter Item Number:')
        if item_id.lower() == 'end':
            break
        if item_id in odata:
            print('The item number already exist please Enter another')
            continue
        elif item_id not in odata:
            name = input('Enter Item name:')
            price = int(input('Enter Item price:'))
            units = int(input('Enter Number of Items in stock:'))
            data[item_id] = [name, price, units]
        cont = input('Do you want to continue (Y/N):').lower()
        if cont == 'y':
            cont = True
        else:
            cont = False
    Update(data, stock)


# function to update the already existing item
def UpdateItems():
    data = {}
    cont = True
    while cont:
        item_id = input('Enter Item Number:')
        if item_id.lower() == 'end':
            break
        name = input('Enter Item name:')
        price = int(input('Enter Item price:'))
        units = int(input('Enter Number of Items in stock:'))
        data[item_id] = [name, price, units]
        cont = input('Do you want to continue (Y/N):').lower()
        if cont == 'y':
            cont = True
        else:
            cont = False
    odata = Scan(stock)
    Update(data, stock)


# function for updating the item's available units and also show to user the appropriate bill for his purchase
def Sale():
    totalAmount = 0
    cont = True
    while cont:
        stockdata = Scan(stock)
        saledata = Scan(sales)
        print('', 'ID'.center(idlen), 'Name'.center(namelen), '', sep='|')
        for i in stockdata:
            print('', str(i).center(idlen),
                  str(saledata[i][0]).center(namelen), '', sep='|')
        print('\n')
        item_id = input('Enter Item Number:')
        if item_id.lower() == 'end':
            break
        elif item_id not in stockdata:
            print('The item number does not exist please Enter another')
            continue

        units = int(input('Enter Number of units:'))
        if stockdata[item_id][2] == 0:
            print('Sorry we don\'t have any more', stockdata[item_id][0], 'we are out of stock')
            o = {item_id: stockdata[item_id][0]}
            Update(o, out_of_stock)
            continue
        elif units > stockdata[item_id][2]:
            print(units, 'units not available only', stockdata[item_id][2], 'available')
            units = stockdata[item_id][2]
            o = {item_id: stockdata[item_id][0]}
            Update(o, out_of_stock)
        elif units == stockdata[item_id][2]:
            units = stockdata[item_id][2]
            o = {item_id: stockdata[item_id][0]}
            Update(o, out_of_stock)

        amount = units * stockdata[item_id][1]

        print('Do you want to buy', units, stockdata[item_id][0])
        buy = input('It would cost you ' + str(amount) + ' would you like to buy (Y/N)').lower()
        if buy == 'y' and units != 0:
            totalAmount += amount
            deltastock = {item_id: [stockdata[item_id][0], stockdata[item_id][1], - units]}
            purchase = {item_id: [stockdata[item_id][0], stockdata[item_id][1], units, amount]}
            Update(purchase, bill, add=True, indices=[1, 2])
            sale = {item_id: [stockdata[item_id][0], stockdata[item_id][1], units, amount]}
            if item_id in saledata:
                Update(sale, sales, add=True, indices=[2, 3])
            else:
                Update(sale, sales)
            Update(deltastock, stock, add=True, indices=[2])
        elif buy == 'n':
            pass
        cont = input('Do you want to continue (Y/N):').lower()
        if cont == 'y':
            cont = True
        else:
            cont = False
            print('Bill')
            billdata = Scan(bill)
            print('', 'ID'.center(idlen), 'Name'.center(namelen), 'Price'.center(numberlen), 'Qty'.center(qtylen), 'Amount'.center(numberlen), '', sep='|')
            for i in billdata:
                print('', str(i).center(idlen),
                      str(billdata[i][0]).center(namelen),
                      str(billdata[i][1]).center(numberlen),
                      str(billdata[i][2]).center(qtylen),
                      str(billdata[i][3]).center(numberlen), '', sep='|')

                # print('|', 'id:', i,
                #       '|', 'name:', billdata[i][0],
                #       '|', 'qty:', billdata[i][1],
                #       '|', 'amount:', billdata[i][2], '|', sep='')

    b = open(bill, 'w')
    b.write('{}')
    b.close()


# function to read stock.txt and output in a table format
def ViewStock():
    stockdata = Scan(stock)

    print('', 'ID'.center(idlen), 'Name'.center(namelen), 'Price'.center(numberlen), 'Qty'.center(qtylen), '', sep='|')
    for i in stockdata:
        print('', str(i).center(idlen),
              str(stockdata[i][0]).center(namelen),
              str(stockdata[i][1]).center(numberlen),
              str(stockdata[i][2]).center(qtylen), '', sep='|')
        # print('|', 'id:', i,
        #       '|', 'name:', stockdata[i][0],
        #       '|', 'price:', stockdata[i][1],
        #       '|', 'qty:', stockdata[i][2], '|', sep='')


# function to read sales.txt and and output total turnover
def TotalSale():
    saledata = Scan(sales)
    print('Total sales')
    print('\n')
    print('', 'ID'.center(idlen), 'Name'.center(namelen), 'Price'.center(numberlen), 'Qty'.center(qtylen), 'Amount'.center(numberlen), '', sep='|')
    for i in saledata:
        print('', str(i).center(idlen),
              str(saledata[i][0]).center(namelen),
              str(saledata[i][1]).center(numberlen),
              str(saledata[i][2]).center(qtylen),
              str(saledata[i][3]).center(numberlen), '', sep='|')

        # print('|', 'id:', i,
        #       '|', 'name:', saledata[i][0],
        #       '|', 'price:', saledata[i][1],
        #       '|', 'qty:', saledata[i][2],
        #       '|', 'amount:', saledata[i][3], sep='')
    print('\n')
    amounts = [saledata[i][3] for i in saledata]
    print('Total turnover:', sum(amounts), sep='')


def RestockLedger():
    itemsToBeRestocked = Scan(out_of_stock)
    newLedger = {i: itemsToBeRestocked[i] for i in itemsToBeRestocked}
    if len(itemsToBeRestocked) == 0:
        print('No items need to be restocked')
    else:
        print('', 'ID'.center(idlen), 'Name'.center(namelen), '', sep='|')
        for i in itemsToBeRestocked:
            stockdata = Scan(stock)
            itemsToBeRestocked = Scan(out_of_stock)
            print('', str(i).center(idlen),
                  str(itemsToBeRestocked[i]).center(namelen), '', sep='|')

            if stockdata[i][2] > 0:
                x = input('The item is already restocked do you want to update the ledger (Y/N):').lower()
                if x == 'y':
                    del newLedger[i]
                else:
                    pass

        f = open(out_of_stock, 'w')
        f.write(json.dumps(newLedger))
        f.close()


# main loop
choice = ''
while True:
    print("""
choices:
1)Sale
2)Add Items
3)Update Stock
4)View Stock
5)Total Sales
6)Restock Ledger
7)End
      """)

    choice = input('Enter your Choice:').lower()

    # block of if and elif statements to call the appropriate functions

    if choice.startswith('sale') or choice.startswith('1'):
        Sale()
    elif choice.startswith('add') or choice.startswith('2'):
        AddItems()
    elif choice.startswith('update') or choice.startswith('3'):
        UpdateItems()
    elif choice.startswith('view') or choice.startswith('4'):
        ViewStock()
    elif choice.startswith('total') or choice.startswith('5'):
        TotalSale()
    elif choice.startswith('Restock') or choice.startswith('6'):
        RestockLedger()
    elif choice.startswith('end') or choice.startswith('7'):
        break
