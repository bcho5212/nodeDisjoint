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
    def __init__(self, search_string=str()):
        self.search_string = search_string
        self.file_df = pandas.DataFrame
        self.address_dict = dict()
        self.prepare_data_frame()
        self.load_address_library()

    def prepare_data_frame(self):
        file_path = read_file.get_file_path(self.search_string)
        file_extension = read_file.get_file_extension(file_path)
        if file_extension == ".csv":
            self.file_df = pandas.read_csv(file_path)
        elif file_extension == ".xlsx":
            self.file_df = pandas.read_excel(file_path)
        else:
            return False
        self.address_dict = self.file_df.to_dict(orient="index")

    def load_address_library(self):
        n = 0
        for row in self.address_dict:
            self.address_dict[row]["kiosk_id"] = n
            self.address_dict[row]["tagged"] = False
            n += 1


if __name__ == "__main__":
    # prepare_address_library("/Users/bcho/IdeaProjects/nodeDisjoint/test/fixtures/Kiosk Coords.csv")
    address_library = AddressLibrary("Kiosk Coords")
    print(address_library.address_dict)
