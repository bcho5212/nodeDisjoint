import os
import glob


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# BUCKET_PATH would be an environment variable that is used to specify where the kiosk file would be dropped
if os.getenv("BUCKET_PATH") is None:
    # bucket_path = "/Users/bcho/IdeaProjects/nodeDisjoint/test/fixtures/"
    bucket_path = ROOT_DIR.replace("mapping", "") + "test/fixtures/"
    output_path = ROOT_DIR.replace("mapping", "") + "test/output/"
else:
    bucket_path = os.getenv("BUCKET_PATH")


def get_file_extension(file_path):
    file_split = os.path.splitext(file_path)
    file_extension = file_split[1]
    return file_extension


def get_file_path(search_string):
    file_list = glob.glob(os.path.join(bucket_path, search_string + "*"))
    file_path = max(file_list, key=os.path.getctime)
    return file_path


if __name__ == "__main__":
    file_path = get_file_path("Kiosk Coords")
    file_extension = get_file_extension(file_path)