from lxml import html
import os
import re
import pandas as pd
import math 
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle


pd.set_option('display.max_columns', None)

folder_path = "data"
paths = os.listdir(folder_path)

file = open(folder_path + "/" + paths[0], 'r',encoding="utf-8")
data = file.read()

result = []

def listToString(s):
    str1 = " "
    return (str1.join(s))

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

    sample = {}
    
    sample["سعر"] = price
    sample["نوع"] = brand
    sample["موديل"] = model
    sample["سنة"] = year

    if features:
        features.append("إضافات")
        if additions:
            additions = listToString(additions).replace(","," ")
            features.append(additions)
        else:
            features.append("null")
        for index,key in enumerate(features[::2]):
            sample[key] = features[1::2][index]
        result.append(sample)
    file.close()

raw_df = pd.DataFrame(result)
raw_df = raw_df.drop(columns=["الدفع"])
raw_df.to_csv("training_data/raw_extracted.csv",index=False)
stage2_df = raw_df.copy()

words = stage2_df['إضافات'].str.split(expand=True).stack()
word_frequency = words.value_counts()
def additions_selected_words_encoder(additions_df,df):
    selected_terms = ["مسجل","مُكيّف","إغلاق مركزي","جنطات مغنيسيوم","وسادة حماية هوائية","جهاز إنذار","فرش جلد","فتحة سقف","بانوراما"]
    for word in selected_terms:
        df[word] = additions_df.str.contains(word).astype("int8")
    return df  

stage2_df = additions_selected_words_encoder(stage2_df['إضافات'],stage2_df) 
stage2_df = stage2_df.drop(columns=["إضافات"])

columns = list(stage2_df.columns)
columns.remove("سعر")
columns.remove("نوع")
columns.remove("موديل")
columns.remove("سنة")
columns.remove("لون السيارة")
columns.remove("قوة الماتور")

def get_number_from_string(string):
   numbers = re.findall(r'\d+', string)
   total = sum(int(num) for num in numbers)
   return total

def extract_num(value):
    number = get_number_from_string(str(value))
    if number:
        return number
    return 5

stage2_df["عدد الركاب"] = stage2_df["عدد الركاب"].apply(extract_num)

def convert_car_meter(value):

    number = re.findall(r'\d+', str(value))

    if(not number):
        return None
    number = number[0]
    
    if (float(number) / 1000) >=1:
        return int(number)
    
    return int(number)*1000

stage2_df["عداد السيارة"] = stage2_df["عداد السيارة"].apply(convert_car_meter)

kilometers_per_liter = {
"بنزين":{
        "less":10.8,
        "more":7.7
},"ديزل":{
        "less":9.7,
        "more":5.6
}
}
amount_of_fuel_per_month = {
  "بنزين":{
        "less":159,
        "more":270
},"ديزل":{
        "less":389,
        "more":841
}  
}

today = datetime.date.today()
year = today.year
fuel_keys = ["بنزين","ديزل"]
for index, row in stage2_df.iterrows():
   if math.isnan(row["عداد السيارة"]) or row["عداد السيارة"] == 0:
        new_value = int()
        cc = int()
        if int(row["قوة الماتور"]) > 2500:
            cc = "more"
        else:
            cc = "less"
        if not row["نوع الوقود"].strip() in fuel_keys:
            new_value = (year - int(row["سنة"]))*12*1500
        else:
            Kvalue = kilometers_per_liter[row["نوع الوقود"].strip()][cc]
            Fvalue = amount_of_fuel_per_month[row["نوع الوقود"].strip()][cc]
            denominator = int(int(row["سنة"])/995)
            new_value = ((year - int(row["سنة"]))*12*Fvalue*Kvalue)/denominator
        stage2_df.at[index, "عداد السيارة"] = int(new_value)

regex_mapping = {
    "شرك":1,
    "صفر":0,
    "اول":1,
    "أول":1,
    "ثان":2,
    "تان":2,
    "ثال":3,
    "تال":3,
    "راب":4,
    "خام":5,
    "ساد":6,
    "ساب":7,
    "ثام":8,
    "تام":8,
    "تاس":9,
    "عاش":10,
    "مست":1,
    "غير":0,
    "مش":0,
    "نفس":1,
}

for index, row in stage2_df.iterrows():
        new_value = None
        text = str(row["أصحاب سابقون"])
        for key,value in regex_mapping.items():
            match = re.search(key,text)
            if(match):
                new_value = value
                continue
        if get_number_from_string(text) > 0:   
            new_value = get_number_from_string(text)
        else:
             new_value = int((year - int(row["سنة"]))/10)
        stage2_df.at[index, "أصحاب سابقون"] = new_value

stage2_df[["سعر", "سنة", "قوة الماتور", "أصحاب سابقون"]] = stage2_df[["سعر", "سنة", "قوة الماتور", "أصحاب سابقون"]].apply(pd.to_numeric)

stage2_df.to_csv("training_data/stage2.csv",index=False)

stage3_df = stage2_df.copy()

columns_names_arabic_english = {
    "سعر":"Price",
    "نوع":"Brand",
    "موديل":"Model",
    "سنة":"Year",
    "لون السيارة":"Color",
    "نوع الوقود":"Fuel_Type",
    "أصل السيارة":"Vehicle_History",
    "رخصة السيارة":"Licence",
    "نوع الجير":"Transmission_Type",
    "الزجاج":"Windows_Type",
    "قوة الماتور":"Engine_Capacity",
    "عداد السيارة":"Kilometers_Driven",
    "عدد الركاب":"Seats",
    "وسيلة الدفع":"Payment_Method",
    "معروضة":"Listed_For",
    "أصحاب سابقون":"Previous_Owners",
    "مسجل":"Radio",
    "CD":"CD",
    "مُكيّف":"Air_Conditioner",
    "إغلاق مركزي":"Central_Lock",
    "وسادة حماية هوائية":"Airbag",
    "جنطات مغنيسيوم":"Magnesium_Rims",
    "جهاز إنذار":"Alert_System",
    "فرش جلد":"Leather_Seats",
    "فتحة سقف":"Sunroof",
    "بانوراما":"Panoramic Sunroof"
}

stage3_df = stage3_df.rename(columns=columns_names_arabic_english)

arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
english_numbers = '0123456789'
translate_arabic_numbers = str.maketrans(arabic_numbers, english_numbers)
stage3_df["Model"] = stage3_df["Model"].str.translate(translate_arabic_numbers)

stage3_df["Model_Is_Year"] =  stage3_df["Model"] == stage3_df["Year"].astype("string")
stage3_df = stage3_df[stage3_df['Model_Is_Year'] != True]
stage3_df = stage3_df.drop(columns=["Model_Is_Year"]).reset_index(drop=True)

stage3_df = stage3_df.drop_duplicates().reset_index(drop=True)

categorical_cols= stage3_df.select_dtypes(include=['object']).columns
numerical_cols = stage3_df.select_dtypes(include=np.number).columns.tolist()
binary_features = ["Panoramic Sunroof", "Sunroof","Leather_Seats","Alert_System","Magnesium_Rims","Airbag","Central_Lock","Air_Conditioner","Radio"]
for bf in binary_features: numerical_cols.remove(bf)

threshold = 1000000
outliers = stage3_df[stage3_df["Kilometers_Driven"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

threshold = 10
outliers = stage3_df[stage3_df["Previous_Owners"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

threshold = 60
outliers = stage3_df[stage3_df["Seats"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

threshold = 7000
outliers = stage3_df[stage3_df["Engine_Capacity"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

threshold = 1981
outliers = stage3_df[stage3_df["Year"] < threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

outliers = stage3_df[(stage3_df["Year"] > 2020) & (stage3_df["Kilometers_Driven"] > 50000)]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

stage3_df["Licence"] = stage3_df["Licence"].str.strip()
stage3_df["Licence"] = stage3_df["Licence"].map({
    "فلسطينية": 1,
    "نمرة صفراء": 0
})

stage3_df["Windows_Type"] = stage3_df["Windows_Type"].str.strip()
stage3_df["Windows_Type"] = stage3_df["Windows_Type"].map({
    "الكتروني": 1,
    "يدوي": 0
})

stage3_df["Payment_Method"] = stage3_df["Payment_Method"].str.strip()
stage3_df["Payment_Method"] = stage3_df["Payment_Method"].map({
    "نقدا فقط": 0,
    "إمكانية التقسيط": 1
})

stage3_df = stage3_df.rename(columns={
    "Licence":"Palestinian_Licence",
    "Windows_Type":"Electric_Windows",
    "Payment_Method":"Installment_Payment_Method"
    })

l, optimal_lambda = stats.boxcox(np.array(stage3_df['Kilometers_Driven']))
stage3_df['Kilometers_Driven_boxcox'] = stats.boxcox(stage3_df['Kilometers_Driven'], lmbda=optimal_lambda)
stage3_df['Kilometers_Driven_boxcox'].plot(kind="hist",title="Kilometers Driven",xlabel="Values")

stage3_df['Previous_Owners_Ranges'] = pd.cut(stage3_df['Previous_Owners'], bins=[-1, 2, 4, 100], labels=['[0-2]', '[3-4]', '[5+)'])
stage3_df['Previous_Owners_Labels'] = pd.cut(stage3_df['Previous_Owners'], bins=[-1, 2, 4, 100], labels=[1, 2, 3])

stage3_df['Seats_Ranges'] = pd.cut(stage3_df['Seats'], bins=[-1, 1, 3,6,8,100], labels=['[1]', '[2]', '[3-5]', '[6-7]', '[8+)'])
stage3_df['Seats_Labels'] = pd.cut(stage3_df['Seats'], bins=[-1, 1, 3,6,8,100], labels=[1, 2, 3, 4, 5])

threshold = 4000
outliers = stage3_df[stage3_df["Engine_Capacity"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

threshold = 200000
outliers = stage3_df[stage3_df["Price"] > threshold]

stage3_df = stage3_df.drop(outliers.index).reset_index(drop=True)

brand_le = LabelEncoder()
brand_labels = brand_le.fit_transform(stage3_df['Brand'])

brand_onehot = OneHotEncoder()
brand_feature_arr = brand_onehot.fit_transform(
                              stage3_df[['Brand']]).toarray()

brand_onehot_feature_labels = list(brand_le.classes_)

brand_onehot_features = pd.DataFrame(brand_feature_arr, 
                            columns=brand_onehot_feature_labels)

stage3_df = pd.concat([stage3_df[stage3_df.columns],brand_onehot_features],axis=1)

model_le = LabelEncoder()
model_labels = model_le.fit_transform(stage3_df['Model'])

model_onehot = OneHotEncoder()
model_feature_arr = model_onehot.fit_transform(
                              stage3_df[['Model']]).toarray()

model_onehot_feature_labels = ['Model_'+str(label)
                           for label in model_le.classes_]

model_onehot_features = pd.DataFrame(model_feature_arr, 
                            columns=model_onehot_feature_labels)
stage3_df = pd.concat([stage3_df[stage3_df.columns],model_onehot_features],axis=1)

stage3_df = stage3_df.drop(columns=["Color","Magnesium_Rims","Listed_For"]).reset_index(drop=True)

fuel_type_le = LabelEncoder()
fuel_type_labels = fuel_type_le.fit_transform(stage3_df['Fuel_Type'])

fuel_type_onehot = OneHotEncoder()
fuel_type_feature_arr = fuel_type_onehot.fit_transform(
                              stage3_df[['Fuel_Type']]).toarray()

fuel_type_onehot_feature_labels = list(fuel_type_le.classes_)

fuel_type_onehot_features = pd.DataFrame(fuel_type_feature_arr, 
                            columns=fuel_type_onehot_feature_labels)

fuel_type_onehot_features["كهرباء "] = fuel_type_onehot_features["كهرباء "]*2.5
fuel_type_onehot_features["هايبرد "] = fuel_type_onehot_features["هايبرد "]*1.5

stage3_df = pd.concat([stage3_df[stage3_df.columns],fuel_type_onehot_features],axis=1)

vehicle_history_le = LabelEncoder()
vehicle_history_labels = vehicle_history_le.fit_transform(stage3_df['Vehicle_History'])

vehicle_history_onehot = OneHotEncoder()
vehicle_history_feature_arr = vehicle_history_onehot.fit_transform(
                              stage3_df[['Vehicle_History']]).toarray()

vehicle_history_onehot_feature_labels = list(vehicle_history_le.classes_)

vehicle_history_onehot_features = pd.DataFrame(vehicle_history_feature_arr, 
                            columns=vehicle_history_onehot_feature_labels)

stage3_df = pd.concat([stage3_df[stage3_df.columns],vehicle_history_onehot_features],axis=1)

transmission_type_le = LabelEncoder()
transmission_type_labels = transmission_type_le.fit_transform(stage3_df['Transmission_Type'])

transmission_type_onehot = OneHotEncoder()
transmission_type_feature_arr = transmission_type_onehot.fit_transform(
                              stage3_df[['Transmission_Type']]).toarray()

transmission_type_onehot_feature_labels = list(transmission_type_le.classes_)

transmission_type_onehot_features = pd.DataFrame(transmission_type_feature_arr, 
                            columns=transmission_type_onehot_feature_labels)

stage3_df = pd.concat([stage3_df[stage3_df.columns],transmission_type_onehot_features],axis=1)


test_df = stage3_df.copy()
test_df = test_df.drop(columns=["Brand","Model","Fuel_Type","Transmission_Type","Vehicle_History","Previous_Owners_Ranges","Previous_Owners","Kilometers_Driven","Seats","Seats_Ranges"]).reset_index(drop=True)


Y = test_df["Price"].to_numpy()
columns = test_df.columns.to_list()
columns.remove("Price")
X = test_df[columns].to_numpy()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 95)

kNN_regressor = KNeighborsRegressor(n_neighbors=5)
kNN_regressor.fit(X_train,Y_train)

kNN_pickle_file = "kNN_regression_model_object.pkl"  

with open(kNN_pickle_file, 'wb') as file:  
    pickle.dump(kNN_regressor, file)