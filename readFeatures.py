from lxml import html
import os
import re
folderPath = "data"
paths = os.listdir(folderPath)
res = []
counter = 1
for path in paths:
    print(counter,"/6864")
    file = open(folderPath + "/" + path, 'r',encoding="utf-8")
    data = file.read()
    tree = html.fromstring(data)
    brand = tree.xpath('//table[@class="driving-table"]//h3/text()')
    yearAndPrice = tree.xpath('//table[@class="driving-table"]//h5/text()')
    if not yearAndPrice or not brand:
        continue
    model = brand[0].split(" ")[1]
    brand = brand[0].split(" ")[0]
    year = yearAndPrice[0]
    year = str(re.findall(r'\d+',year)[0])
    price = yearAndPrice[1]
    price = str(re.findall(r'\d+',price)[0])
    headers = ["brand","model","year","price"]
    res += brand + "," + model + "," + year + "," + price + "\n"
    file.close()
    counter += 1
newFile = open("test.csv","x",encoding="utf-8")
for index,header in enumerate(headers):
    if(index != 0):
        newFile.write(",")
    newFile.write(header)
newFile.write("\n")
newFile.writelines(res)
newFile.close()

# Removing Redundant data
counter = 1
in_file = open('test.csv','r',encoding="utf-8")
out_file = open('new_test.csv','w',encoding="utf-8")
seen = set()
for line in in_file:
   print(counter,"/5721")
   if line in seen:
       continue
   seen.add(line)
   out_file.write(line)
   counter += 1
in_file.close()
out_file.close()