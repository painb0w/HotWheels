import os
import gzip
import shutil

def extract_gz_files(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith(".gz"):
            gz_file_path = os.path.join(source_folder, filename)
            output_file_path = os.path.join(destination_folder, filename[:-3])  

            try:
                with gzip.open(gz_file_path, 'rb') as gz_file:
                    with open(output_file_path, 'wb') as output_file:
                        shutil.copyfileobj(gz_file, output_file)
                print(f"Распакован: {filename} -> {output_file_path}")
            except Exception as e:
                print(f"Ошибка при распаковке {filename}: {e}")


