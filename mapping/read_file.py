import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# BUCKET_PATH would be an environment variable that is used to specify where the kiosk file would be dropped
if os.getenv("BUCKET_PATH") is None:
    bucket_path = ROOT_DIR.replace("mapping", "") + "test/fixtures/"
    output_path = ROOT_DIR.replace("mapping", "") + "test/output/"
else:
    bucket_path = os.getenv("BUCKET_PATH")


# Get the file extension to know which pandas function to use
def get_file_extension(file_path):
    file_split = os.path.splitext(file_path)
    file_extension = file_split[1]
    return file_extension
