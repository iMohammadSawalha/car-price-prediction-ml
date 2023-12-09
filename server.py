
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from transformation_functions import *
from flask import Flask,request
import pickle

kNN_pickle_file = "kNN_regression_model.pkl"  
with open(kNN_pickle_file, 'rb') as file:  
    kNN_Model = pickle.load(file)

def transform_to_df_from_dict(dict):

    dict["kilometers_driven"] = convert_car_meter(dict["kilometers_driven"])

    dict["seats"] = extract_num_seats(dict["seats"])

    dict["previous_owners"] = convert_previous_owners_to_num(dict["previous_owners"])

    df = pd.DataFrame([dict])
    
    brand_le = LabelEncoder()
    brand_labels = brand_le.fit_transform(df['brand'])
    df = one_hot_enconde_df(df,"brand",list(brand_le.classes_))

    model_le = LabelEncoder()
    model_labels = model_le.fit_transform(df['model'])
    model_onehot_feature_labels = ['Model_'+str(label)
                           for label in model_le.classes_]
    df = one_hot_enconde_df(df,"model",model_onehot_feature_labels)

    fuel_type_le = LabelEncoder()
    fuel_type_labels = fuel_type_le.fit_transform(df['fuel_type'])
    df = one_hot_enconde_df(df,"fuel_type",list(fuel_type_le.classes_))

    vehicle_history_le = LabelEncoder()
    vehicle_history_labels = vehicle_history_le.fit_transform(df['vehicle_history'])
    df = one_hot_enconde_df(df,"vehicle_history",list(vehicle_history_le.classes_))

    transmission_type_le = LabelEncoder()
    transmission_type_labels = transmission_type_le.fit_transform(df['transmission_type'])
    df = one_hot_enconde_df(df,"transmission_type",list(transmission_type_le.classes_))
    

    df["licence"] = df["licence"].str.strip()
    df["licence"] = df["licence"].map(licence_map)


    df["windows_type"] = df["windows_type"].str.strip()
    df["windows_type"] = df["windows_type"].map(windows_type_map)

    df["payment_method"] = df["payment_method"].str.strip()
    df["payment_method"] = df["payment_method"].map(payment_method_map)

    df = df.rename(columns={
    "licence":"palestinian_licence",
    "windows_type":"electric_windows",
    "payment_method":"installment_payment_method"
    })

    df["kilometers_driven_boxcox"] = convert_kilometers_driven_boxcox(df["kilometers_driven"])

    df["seats_labels"] = bin_seats(df["seats"])

    df["previous_owners_labels"] = bin_previous_owners(df["previous_owners"])


    resulted_df = pd.DataFrame(data=[np.zeros(len(features_columns_names))],columns=features_columns_names)
    
    resulted_df[df.columns] = df[df.columns].iloc[:1]

    return resulted_df

def predict_price(df):
    return kNN_Model.predict(df)[0]

app = Flask(__name__)

@app.route("/",methods=["POST"])
def hello():
    df = transform_to_df_from_dict(request.get_json())
    df = df.drop(columns=["brand","model","fuel_type","transmission_type","vehicle_history","previous_owners_ranges","previous_owners","kilometers_driven","seats","seats_ranges","licence","windows_type","payment_method"]).reset_index(drop=True)
    df = df[features_final_order]
    return str(round(predict_price(df)))



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
