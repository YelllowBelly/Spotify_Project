import pandas as pd
import numpy as np

data_2020 = pd.read_csv('2020spotify_results.csv')
data_2020 = data_2020.dropna()

def is_grammy(string_name):
    #lowercase/strip
    string_name = string_name.lower()
    string_name = string_name.strip()

    grammy_2020_list = ['black parade','the box',
    'cardigan','circles','don\'t start now','everything i wanted',
    'i can\'t breathe','if the world was ending']

    #save desired rows, make others null
    if(string_name in grammy_2020_list):
        return string_name
    else:
        return None

#extract grammy data from dataset
grammy_2021_data = data_2020
grammy_2021_data ['name'] = grammy_2021_data['name'].apply(is_grammy)
grammy_2021_data = grammy_2021_data.dropna()
print(grammy_2021_data['name'].unique())
