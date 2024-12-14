import parse_data
import unzip
import config
import preprocess_data
import pandas as pd

source_folder_Pavel = "C:/University/5 semester/ml projects/final project/Выборки"  # Сюда парсер скачивает выборки
destination_folder_Pavel = "C:/Users/Pavel/Documents/GitHub/HotWheels/Выборки"  # Сюда парсер распаковывает архивы из source_folder
source_folder_Artyom = r"D:\Университет\3 курс 5 семестр\МиТМО (машинки(тачки))\проект\data"
destination_folder_Artyom = r"D:\Университет\3 курс 5 семестр\МиТМО (машинки(тачки))\проект\HotWheels\Выборки"

parse_data.get_weather_archive(source_folder_Artyom)
unzip.extract_gz_files(source_folder_Artyom, destination_folder_Artyom)

# parse_data.get_weather_archive(config.source_folder)
# unzip.extract_gz_files(config.source_folder, config.destination_folder)

df_weather = preprocess_data.get_weather_all('C:/Users/Pavel/Documents/GitHub/HotWheels/Выборки/временная') 
df_fires = preprocess_data.get_fires_all(config.fires_path)
df = preprocess_data.merge_fires_weather(df_fires, df_weather, config.destination_file_result)

print(df.info())