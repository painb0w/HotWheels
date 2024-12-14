import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

def get_weather_all(directory): #указать в качестве параметра папку с выборками погоды
    df_weather_list = []

    for filename in os.listdir(directory):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):  
            file_path = os.path.join(directory, filename)
            town = pd.read_excel(file_path)
            town=town.columns[0].split()[2].replace(',', '')            
            df_weather = pd.read_excel(file_path, skiprows=6)
            df_weather['Населенный пункт']=town
            df_weather.columns.values[0] = 'Местное время'
            df_weather['Местное время'] = pd.to_datetime(df_weather['Местное время'], format='%d.%m.%Y %H:%M')
            df_weather = df_weather[df_weather['Местное время'].dt.hour == 14]
            df_weather['Местное время'] = df_weather['Местное время'].dt.date
            df_weather = df_weather[['Местное время', 'Населенный пункт', 'T', 'P', 'U', 'DD', 'Ff', 'N', 'WW', 'Cl', 'Cm', 'Nh']]
            df_weather.Cm = df_weather.Cm.fillna('Высококучевых, высокослоистых или слоисто-дождевых облаков нет.')
            df_weather.Cl = df_weather.Cl.fillna('Слоисто-кучевых, слоистых, кучевых или кучево-дождевых облаков нет.')
            df_weather.Nh = df_weather.Nh.fillna('Осадков нет.')
            df_weather.N = df_weather.N.fillna('Облаков нет.')

            df_weather_list.append(df_weather)

    final_df = pd.concat(df_weather_list, ignore_index=True)
    return final_df

def get_fires_all(fires_path): # указать в качестве параметра файл с выборкой пожаров
    df = pd.read_csv(fires_path)
    return df

def merge_fires_weather(fires_df, weather_df, destination_file_result):
    """
    Метод для получения итогового датасета, на котором будет обучаться модель

    fires_df, weather_df - датасеты пожаров и погоды соответственно
    destination_file_result - сюда сохранится обработанная объединенная выборка, готовая к обучению на ней модели 
    """
    weather_df['Местное время'] = pd.to_datetime(weather_df['Местное время'])
    fires_df['dt'] = pd.to_datetime(fires_df['dt'])
    result = pd.merge(fires_df, weather_df, right_on=['Местное время', 'Населенный пункт'], left_on=['dt', 'Только населенный пункт'], how='left')
    result = result.dropna()
    result = result[['Местное время', 'Населенный пункт', 'type_id', 
       'T', 'P', 'U', 'DD', 'Ff', 'N', 'WW', 'Cl', 'Cm', 'Nh']]
    result.to_csv(destination_file_result, index=False) # Сохраняем датасет в файл csv 
    return result

def prepare_for_clasterization(df): 

    scaler = MinMaxScaler() 

    encoder1 = LabelEncoder()
    encoder2 = LabelEncoder()
    encoder3 = LabelEncoder()
    encoder4 = LabelEncoder()
    encoder5 = LabelEncoder()
    encoder6 = LabelEncoder()
    encoder7 = LabelEncoder()

    result = df.copy()

    result[['T','P','U', 'Ff']] = scaler.fit_transform(result[['T','P','U', 'Ff']])

    result['year'] = result['Местное время'].dt.year
    result['month'] = result['Местное время'].dt.month
    result = result.drop(columns={'Местное время'})

    result['Населенный пункт'] = encoder1.fit_transform(result['Населенный пункт'])
    result['DD'] = encoder2.fit_transform(result['DD'])
    result['N'] = encoder3.fit_transform(result['N'])
    result['WW'] = encoder4.fit_transform(result['WW'])
    result['Cl'] = encoder5.fit_transform(result['Cl'])
    result['Cm'] = encoder6.fit_transform(result['Cm'])
    result['Nh'] = encoder7.fit_transform(result['Nh'])
    
    interpratations = [encoder1.classes_, encoder2.classes_, encoder3.classes_, encoder4.classes_, encoder5.classes_, encoder6.classes_, encoder7.classes_]

    return result, interpratations

# def get_final_df(destination_file_result): # считывает в датафрейм итоговый датасет и возвращает его
#     final_df = pd.read_csv(destination_file_result)
#     return final_df


