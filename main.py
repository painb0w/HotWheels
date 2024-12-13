import parse_data
import unzip

source_folder_Pavel = "C:/University/5 semester/ml projects/final project/Выборки"  # Сюда парсер скачивает выборки
destination_folder_Pavel = "C:/Users/Pavel/Documents/GitHub/HotWheels/Выборки"  # Сюда парсер распаковывает архивы из source_folder
source_folder_Artyom = "D:/Университет/3 курс 5 семестр/МиТМО (машинки(тачки))/проект/data"
destination_folder_Artyom = "D:/Университет/3 курс 5 семестр/МиТМО (машинки(тачки))/проект/HotWheels/Выборки"

parse_data.get_weather_archive(source_folder_Artyom)
unzip.extract_gz_files(source_folder_Artyom, destination_folder_Artyom)
