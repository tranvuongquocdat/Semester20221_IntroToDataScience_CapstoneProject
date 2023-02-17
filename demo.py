import streamlit as st
import joblib
import pandas as pd
import numpy as np
from utils import transform_score
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import matplotlib.pyplot as plt
import shap
shap.initjs()

st.write("# Laptop Price Prediction")

weight = st.slider("Weight (kg)", 0.0, 5.0, step = 0.01)

laptop_brand = st.selectbox("Laptop brand",["Lenovo","Dell","Asus", "HP", "MSI", "Acer", "LG", "GIGABYTE","Apple", "Razer", "Samsung", "Microsoft", "Huawei", "AVITA", "Xiaomi", "Colorful", "Other"])

battery = st.slider("Battery capacity (mWh)", 0.0, 100.0)

monitor_size = st.slider("Monitor size", 5.0, 20.0)

ram_type = st.selectbox("Type of your RAM",["DDR4","DDR5", "LPDDR4x", "LPDDR5", "LPDDR3", "DDR3L", "LPDDR3L"])

ram_capacity = st.number_input("Enter your RAM capacity (GB)")

cpu = st.text_input("Your CPU")

gpu = st.text_input("Your GPU")

HDD_capacity = st.number_input("Enter storage capacity of HDD (MB)")

SSD_capacity = st.number_input("Enter storage capacity of SDD (MB)")

website = st.selectbox("Where is that laptop sold?", ["thinkpro", "laptop88", "Other"])

columns= ['battery', 'weight', 'monitor_size', 'ram_capacity', 'SSD_capacity',
       'cpu_core_num', 'cpu_thread_num', 'avg_bench', 'gamming', 'desktop',
       'workstation', 'gpu_score', 'unknown_gpu', 'website_thinkpro',
       'laptop_brand_Asus', 'laptop_brand_Dell', 'laptop_brand_Lenovo',
       'laptop_brand_Other', 'laptop_brand_Razer']

df_pred = dict()

df_pred['battery'] = battery
df_pred['weight'] = weight
df_pred['monitor_size'] = monitor_size
df_pred['ram_capacity'] = ram_capacity
df_pred['SSD_capacity'] = SSD_capacity

df_pred = pd.DataFrame(df_pred, index=[0])

df_pred[['website_thinkpro',
       'laptop_brand_Asus', 'laptop_brand_Dell', 'laptop_brand_Lenovo',
       'laptop_brand_Other', 'laptop_brand_Razer']] = 0

def website_transform(data):
    if(data=='thinkpro'):
        result = 1
    elif(data=='laptop88'):
        result = 0
    elif data=='Other':
        result = 0
    return(result)

df_pred['website_thinkpro'] = website_transform(website)

def brand_transform(data):
    if data == 'Asus':
        df_pred['laptop_brand_Asus'] = 1          
    elif data == 'Dell':
        df_pred['laptop_brand_Dell'] = 1 
    elif data == 'Lenovo':
        df_pred['laptop_brand_Lenovo'] = 1 
    elif data == 'Razer':
        df_pred['laptop_brand_Razer'] = 1 
    elif data == 'Other':
        df_pred['laptop_brand_Other'] = 1 
brand_transform(laptop_brand)

df_pred['cpu'] = [cpu]
df_pred['gpu'] = [gpu]

df_pred = transform_score(df_pred)

if gpu == '':
    df_pred['unknown_gpu'] = 1
    df_pred['gpu_score'] = np.nan
else:
    df_pred['unknown_gpu'] = 0

df_pred["SSD_capacity"] = df_pred["SSD_capacity"].astype(float)
df_pred["monitor_size"] = df_pred["monitor_size"].astype(float)
df_pred["weight"] = df_pred["weight"].astype(float)
df_pred["battery"] = df_pred["battery"].astype(float)
df_pred["cpu_core_num"] = df_pred["cpu_core_num"].astype(float)
df_pred["cpu_thread_num"] = df_pred["cpu_thread_num"].astype(float)
df_pred["ram_capacity"] = df_pred["ram_capacity"].astype(float)

cols = ['battery', 'weight', 'monitor_size', 'ram_capacity', 'SSD_capacity', 'cpu_core_num', 'cpu_thread_num', 'avg_bench', 'gamming', 'desktop', 'workstation', 'gpu_score', 'unknown_gpu', 'website_thinkpro', 'laptop_brand_Asus', 'laptop_brand_Dell', 'laptop_brand_Lenovo', 'laptop_brand_Other', 'laptop_brand_Razer']

df_pred = df_pred[cols]

numerical_cols = ["battery", 
          "weight", "monitor_size",
          "ram_capacity", 
          "SSD_capacity", 
          "cpu_core_num",
          "cpu_thread_num",
          "avg_bench", "desktop", "workstation" , "gamming",
          "gpu_score",
          "unknown_gpu"]

imptr = joblib.load('na_handler.pkl')
df1_test = df_pred[numerical_cols]
df2_test = pd.DataFrame(imptr.transform(df1_test), columns = df1_test.columns)
df_pred[numerical_cols] = df2_test.values

df_train = pd.read_csv('model/Data used for interpreting/training_set.csv', index_col = 0)
X_train = df_train.drop("price", axis = 1)

scaler = MinMaxScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = scaler.get_feature_names_out())
df_pred_ = df_pred
df_pred = pd.DataFrame(scaler.transform(df_pred), columns = scaler.get_feature_names_out())

model = joblib.load('xgb_model.pkl')
prediction = model.predict(df_pred)

#Get shap values
explainer = shap.Explainer(model)
shap_values = explainer(df_pred)

# print(shap_values)
# shap.plots.force(explainer.expected_value, shap_values.values[0], show=False)
# plt.savefig('force.png', bbox_inches = 'tight')

# shap.plots.waterfall(shap_values[0], max_display=20, show=False)
# plt.savefig('explain.png', bbox_inches = 'tight')

if st.button('Predict'):
    st.markdown(f"# Predicted Price: **:red[{str(prediction[0])}]** VND")
    st.markdown("###### Here is the DataFrame used for modeling:")
    df_pred_

    # fig = plt.figure()
    # shap.force_plot(explainer.expected_value, shap_values.values[0], df_pred.iloc[0,:], show = False)
    # fig

    st.markdown("###### The contribution of each feature to Price:")

    fig = plt.figure()
    shap.plots.waterfall(shap_values[0], max_display=20, show=False)
    fig


