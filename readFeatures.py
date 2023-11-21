from lxml import html
import os
import re

def listToString(s):
 
    # initialize an empty string
    str1 = "|"
 
    # return string
    return (str1.join(s))


folder_path = "data"
paths = os.listdir(folder_path)
res = []
counter = 1
keysMax = 0
keysNames = ""
for path in paths:
    file = open(folder_path + "/" + path, 'r',encoding="utf-8")
    data = file.read()
    tree = html.fromstring(data)
    brand = tree.xpath('//table[@class="driving-table"]//h3/text()')
    year_price = tree.xpath('//table[@class="driving-table"]//h5/text()')
    if not year_price or not brand:
        continue
    features = tree.xpath('//table[@class="list_ads"]//tr[@class="list-row"]//td/text()')[:-3] # The [:-3] is to remove the last 3 items of the list because those are the additions which we are taking seperately
    additions = tree.xpath('//td[@class="list-additions"]//li/text()')
    model = brand[0].split(" ")[1]
    brand = brand[0].split(" ")[0]
    year = year_price[0]
    year = str(re.findall(r'\d+',year)[0])
    price = year_price[1]
    price = str(re.findall(r'\d+',price)[0])
    sample = {
        "سعر":price,
        "شركة":brand,
        "موديل":model,
        "سنة":year,
        "لون السيارة":"null",
        "نوع الوقود":"null",
        "أصل السيارة":"null",
        "رخصة السيارة":"null",
        "نوع الجير":"null",
        "الزجاج":"null",
        "قوة الماتور":"null",
        "عداد السيارة":"null",
        "عدد الركاب":"null",
        "الدفع":"null",
        "وسيلة الدفع":"null",
        "معروضة":"null",
        "أصحاب سابقون":"null",
        "إضافات":"null"
    }
    if features:
        features.append("إضافات")
        if additions:
            features.append(listToString(additions))
        else:
            features.append("null")
        for index,key in enumerate(features[::2]):
            sample[key] = features[1::2][index]
        # features[::2] # keys
        # features[1::2] # values
    headers = ["شركة","موديل","سنة","لون السيارة","نوع الوقود","أصل السيارة","رخصة السيارة","نوع الجير","الزجاج","قوة الماتور","عداد السيارة","عدد الركاب","وسيلة الدفع","معروضة","أصحاب سابقون","إضافات","سعر"]
    res += sample["شركة"] + "," + sample["موديل"] + "," + sample["سنة"] + "," + sample["لون السيارة"] + "," + sample["نوع الوقود"] + "," + sample["أصل السيارة"] + "," + sample["رخصة السيارة"] + "," + sample["نوع الجير"] + "," + sample["الزجاج"] + "," + sample["قوة الماتور"] + "," + sample["عداد السيارة"] + "," + sample["عدد الركاب"] + "," + sample["وسيلة الدفع"] + "," + sample["معروضة"] + "," + sample["أصحاب سابقون"] + "," + sample["إضافات"] + "," +sample["سعر"] + "\n"
    file.close()
    print(counter,"/6864")
    counter += 1
new_file = open("test.csv","x",encoding="utf-8")
for index,header in enumerate(headers):
    if(index != 0):
        new_file.write(",")
    new_file.write(header)
new_file.write("\n")
new_file.writelines(res)
new_file.close()

# Removing Redundant data

counter = 1
old_file = open('test.csv','r',encoding="utf-8")
new_file = open('new_test.csv','w',encoding="utf-8")
seen = set()
for line in old_file:
   print(counter,"/5721")
   if line in seen:
       continue
   seen.add(line)
   new_file.write(line)
   counter += 1
old_file.close()
new_file.close()