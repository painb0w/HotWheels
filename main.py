import parse_data
import unzip
import config
import preprocess_data
import pandas as pd
import model

# parse_data.get_weather_archive(config.source_folder)
# unzip.extract_gz_files(config.source_folder, config.destination_folder)

df_weather = preprocess_data.get_weather_all(config.destination_folder) 
df_fires = preprocess_data.get_fires_all(config.fires_path)
df = preprocess_data.merge_fires_weather(df_fires, df_weather, config.destination_file_result)

result, description = preprocess_data.prepare_for_clasterization(df)

X = result.values

dbscan = model.DBSCAN(eps=14, min_samples=20)
dbscan.fit(X)

dbscan.plot_clusters(X)