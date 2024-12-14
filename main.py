import parse_data
import unzip
import config
import preprocess_data
import pandas as pd

# parse_data.get_weather_archive(config.source_folder)
# unzip.extract_gz_files(config.source_folder, config.destination_folder)

df_weather = preprocess_data.get_weather_all('C:/Users/Pavel/Documents/GitHub/HotWheels/Выборки/временная') 
df_fires = preprocess_data.get_fires_all(config.fires_path)
df = preprocess_data.merge_fires_weather(df_fires, df_weather, config.destination_file_result)

print(df.info())