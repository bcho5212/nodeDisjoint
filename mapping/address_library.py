import pandas

import mapping.read_file as read_file

invalid_kiosks = (
    "Chicago Midway Airport - Ticketing Employee Lounge",
    "Good Samaritan Hospital",
    "Medical College of Wisconsin",
    "Peggy Notebaert Nature Museum",
    "O'Hare Terminal 2 - Gate F6",
    "Good Shepherd Hospital",
    "Allstate HQ (Tenants Only)",
    "MillerCoors HQ",
    "100 E Wisconsin",
    "Moraine Valley Community College: Police Academy- Building B",
)


class AddressLibrary:
    def __init__(self, input_file_path):
        self.file_df = pandas.DataFrame
        self.input_file_path = input_file_path
        self.address_dict = dict()
        self.prepare_data_frame()
        self.load_address_library()

    # Prepare the data frame based on input file
    def prepare_data_frame(self):
        file_extension = read_file.get_file_extension(self.input_file_path)
        if file_extension == ".csv":
            self.file_df = pandas.read_csv(self.input_file_path)
        elif file_extension == ".xlsx":
            self.file_df = pandas.read_excel(self.input_file_path)
        else:
            return False
        self.address_dict = self.file_df.to_dict(orient="index")

    # Load the address library, adding kiosk_id's ad tagged flags to each row
    def load_address_library(self):
        n = 0
        for row in self.address_dict:
            self.address_dict[row]["kiosk_id"] = n
            self.address_dict[row]["tagged"] = False
            n += 1
