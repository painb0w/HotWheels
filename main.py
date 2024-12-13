import parse_data
import unzip

source_folder = "C:/University/5 semester/ml projects/final project/Выборки"  # Сюда парсер скачивает выборки
destination_folder = "C:/Users/Pavel/Documents/GitHub/HotWheels/Выборки"  # Сюда парсер распаковывает архивы из source_folder

parse_data.get_weather_archive(source_folder)
unzip.extract_gz_files(source_folder, destination_folder)
