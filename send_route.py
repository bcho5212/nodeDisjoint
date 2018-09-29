import datetime
from pathlib import Path

import pandas

from mapping.path_mapping import PathMapping
from mapping.read_file import output_path


# Process the input file and generate the routes for each driver
def prepare_routes(number_of_drivers, input_file_path):
    path_mapper = PathMapping(input_file_path)
    path_mapper.execute_path_mapping(number_of_drivers=number_of_drivers)
    return path_mapper


# Create the data frame that will feed into the output csv file
def generate_data_frame(drivers, driver_index):
    driver_kiosk_ids = drivers[driver_index].kiosk_ids
    driver_route = drivers[driver_index].route
    file_dict = dict()
    for stop_number in driver_kiosk_ids:
        kiosk_id = driver_kiosk_ids[stop_number]
        file_dict[stop_number] = {
            "driver_index": driver_index,
            "stop_number": stop_number,
            "name": driver_route[kiosk_id]["name"],
            "address": driver_route[kiosk_id]["address (S)"],
            "latitude (N)": driver_route[kiosk_id]["latitude (N)"],
            "longitude (N)": driver_route[kiosk_id]["longitude (N)"]
        }
    df = pandas.DataFrame.from_dict(
        data=file_dict,
        orient="index",
    )
    return df


# Send the data frame(s) to the output csv file - Creating the file if new and appending if the file exists
def send_routes_to_csv(path_mapper, file_name):
    drivers = path_mapper.driver_dict
    file_check = Path(file_name)
    for driver_index in drivers:
        if driver_index == 0:
            data_frame = generate_data_frame(drivers, driver_index)
            data_frame.to_csv(file_name)
        if driver_index > 0 and file_check.is_file():
            data_frame = generate_data_frame(drivers, driver_index)
            data_frame.to_csv(file_name, mode="a", header=False)


if __name__ == "__main__":
    output_file_name = output_path + str(datetime.date.today()) + "_Driver_Routes.csv"
    input_file_path = input("Path to file: ")
    number_of_drivers = input("Number of drivers: ")
    routes = prepare_routes(int(number_of_drivers), input_file_path)
    send_routes_to_csv(routes, output_file_name)
    print("File with routes has been created at: {0}".format(output_file_name))
