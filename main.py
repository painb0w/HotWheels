import parse_data
import unzip
import config
import preprocess_data
import pandas as pd

# parse_data.get_weather_archive(config.source_folder_Artyom)
# unzip.extract_gz_files(config.source_folder_Artyom, config.destination_folder_Artyom)

# parse_data.get_weather_archive(config.source_folder_Pavel)
# unzip.extract_gz_files(config.source_folder_Pavel, config.destination_folder_Pavel)

df_weather = preprocess_data.get_weather_all(config.destination_folder_Artyom) 
df_fires = preprocess_data.get_fires_all(config.fires_path_Artyom)
df = preprocess_data.merge_fires_weather(df_fires, df_weather, config.destination_file_result_Artyom)

print(df.info())