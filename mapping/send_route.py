import pandas
import datetime

from mapping.path_mapping import PathMapping
from mapping.read_file import output_path
from pathlib import Path


def prepare_routes():
    path_mapper = PathMapping()
    path_mapper.execute_path_mapping(number_of_drivers=2)
    return path_mapper


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
            "address": driver_route[kiosk_id]["address (S)"]
        }
    df = pandas.DataFrame.from_dict(
        data=file_dict,
        orient="index",
    )
    return df


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
    output_file_name = output_path + str(datetime.date.today()) + "_Driver_Routes"
    routes = prepare_routes()
    send_routes_to_csv(routes, output_file_name)