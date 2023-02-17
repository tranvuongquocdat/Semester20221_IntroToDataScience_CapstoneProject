import pandas as pd
import numpy as np
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import matplotlib.pyplot as plt
# import shap

df = pd.DataFrame({"cpu": ["Intel Core i5 11300H"],
                  "gpu": ["intel iris xe graphics"]})

def transform_score(df):

    df_cpu = pd.read_csv("data/cpu_info.csv", index_col=0)
    df_gpu = pd.read_csv('data/gpu_map.txt', sep=":", header=None)
    df_gpu.columns = ["gpu", "gpu_score"]

    df_cpu["number_of_core"] = df_cpu["number_of_core"].str.replace(" Cores", "")
    df_cpu["number_of_thread"] = df_cpu["number_of_thread"].str.replace(" Threads", "")

    def get_cpu_brand(x):
        try:
            if "AMD" in x:
                return "AMD"
            elif "Intel" in x or bool(re.search(r"i.|i .",x)):
                return "Intel"
            elif "Apple" in x:
                return "Apple"
        except:
            return np.nan

    def get_cpu_level(x):
        try:
            match = re.search('i\d{1}|i \d{1}|R\d{1}| \d ', x)
            return match.group(0)
        except:
            return np.nan

    def get_cpu_ver(x):
        try:
            match = re.search('\d{5}\w{2}|\d{5}\w{1}|\d{4}\w{2}|\d{4}\w{1}|\w{1}\d{4}|\d{4}|M1|M2|M1 Pro ', x)
            return match.group(0)
        except:
            return np.nan
        
    df_cpu["brand"] = df_cpu["cpu_name"].apply(get_cpu_brand)
    df_cpu["level"] = df_cpu["cpu_name"].apply(get_cpu_level)
    df_cpu["ver"] = df_cpu["cpu_name"].apply(get_cpu_ver)
    df_cpu = df_cpu.drop_duplicates(subset = ["brand", "level", "ver"], ignore_index = True)
    # print(df_cpu.dtypes)

    df["brand"] = df["cpu"].apply(get_cpu_brand)
    df["level"] = df["cpu"].apply(get_cpu_level).astype(str)
    df["ver"] = df["cpu"].apply(get_cpu_ver).astype(str)
    # print(df.dtypes)
    df = df.merge(df_cpu, how = "left", on = ["level", "ver"])

    df_gpu["gpu"] = df_gpu["gpu"].str.lower()
    df_gpu = df_gpu.drop_duplicates(subset = "gpu",ignore_index = True)
    df_gpu["gpu"] = df_gpu["gpu"].str.replace("®", "").str.replace("™", "")

    def bs_replace(x):
        try:
            return x.replace(u'\xa0', u' ')
        except:
            return x

    df["gpu"] = df["gpu"].str.lower()
    df["gpu"] = df["gpu"].apply(bs_replace)
    df["gpu"] = df["gpu"].str.replace("®", "").str.replace("™", "")
    df["gpu"] = df["gpu"].str.split(r" |-|/|\|")

    df["gpu_score"] = np.nan

    def gpu_process(df):
        for index_gpu, i in enumerate(df["gpu"]):
            for index, a_string in enumerate(df_gpu["gpu"]):
                try:
                    if all(_ in a_string for _ in i):
                        df.loc[index_gpu, "gpu_score"] = df_gpu["gpu_score"].iloc[index]
            
                except:
                    df.loc[index_gpu, "gpu_score"] = np.nan
                    
    gpu_process(df)

    df = df.reset_index(drop = True)
    df.rename(columns = {"number_of_core":"cpu_core_num", "number_of_thread":"cpu_thread_num"}, inplace = True)
    df = df.drop(columns = ["level", "ver", "cpu_name", "brand_x", "brand_y","cpu","gpu"])

    return df

print(df)
print(transform_score(df))
