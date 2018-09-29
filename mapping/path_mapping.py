import operator

import geopy.distance

from mapping.address_library import AddressLibrary
from mapping.driver import Driver


class PathMapping:
    def __init__(self, input_file_path):
        self.driver_dict = dict()
        self.starting_coords = ("41.8851024", "-87.6618988")
        self.coordinates_library = AddressLibrary(input_file_path)
        self.address_library = self.coordinates_library.address_dict
        self.calculate_starting_distance()

    # Generate driver objects based number specified by user
    def initiate_drivers(self, number_of_drivers):
        for n in range(number_of_drivers):
            self.driver_dict[n] = Driver(n)

    # Calculate the initial distance from the starting coordinates for each kiosk
    def calculate_starting_distance(self):
        keys_library = self.generate_keys_library()
        for n in keys_library:
            kiosk_coords = (
                self.address_library[n]["latitude (N)"],
                self.address_library[n]["longitude (N)"]
            )
            distance_from_start = geopy.distance.distance(self.starting_coords, kiosk_coords)
            self.address_library[n]["dist_from_start"] = distance_from_start.km

    # Set the driver's first stop based on the starting distance calculated
    def set_driver_start_point(self):
        list_of_distances = {}
        stop_number = 0
        for driver_index in self.driver_dict:
            keys_library = self.generate_keys_library()
            for n in keys_library:
                list_of_distances[self.address_library[n]["kiosk_id"]] = self.address_library[n]["dist_from_start"]
            kiosk_id = min(list_of_distances.items(), key=operator.itemgetter(1))[0]
            self.driver_dict[driver_index].kiosk_ids[stop_number] = kiosk_id
            self.set_tagged_to_true(kiosk_id)
            list_of_distances.clear()

    # Using the previous coordinates / stop, loop through every kiosk and calculate the distance to that next kiosk
    def calculate_distance_to_next(self, previous_coords):
        keys_library = self.generate_keys_library()
        for n in keys_library:
            kiosk_coords = (
                self.address_library[n]["latitude (N)"],
                self.address_library[n]["longitude (N)"]
            )
            distance_to_next = geopy.distance.distance(previous_coords, kiosk_coords)
            self.address_library[n]["dist_to_next"] = distance_to_next.km

    # Set the driver's next stop based on the distance calculated
    def set_driver_next_point(self, stop_number):
        list_of_distances = {}
        for driver_index in self.driver_dict:
            previous_stop_number = stop_number - 1
            previous_kiosk_id = self.driver_dict[driver_index].kiosk_ids[previous_stop_number]
            previous_coords = self.find_previous_coords(previous_kiosk_id)
            self.calculate_distance_to_next(previous_coords)
            keys_library = self.generate_keys_library()
            for n in keys_library:
                list_of_distances[self.address_library[n]["kiosk_id"]] = self.address_library[n]["dist_to_next"]
            kiosk_id = min(list_of_distances.items(), key=operator.itemgetter(1))[0]
            self.driver_dict[driver_index].kiosk_ids[stop_number] = kiosk_id
            self.set_tagged_to_true(kiosk_id)
            list_of_distances.clear()
            if self.check_if_complete():
                break

    # Based on the previous stop, provide the kiosk coordinates for use
    def find_previous_coords(self, previous_kiosk_id):
        for n in self.address_library:
            if self.address_library[n]["kiosk_id"] == previous_kiosk_id:
                previous_coords = (
                    self.address_library[n]["latitude (N)"],
                    self.address_library[n]["longitude (N)"]
                )
                return previous_coords

    # Generate and refresh the keys_library after every stop is tagged so that there is no issue with visiting the same
    # kiosk multiple times
    def generate_keys_library(self):
        keys_library = (
            n for n in self.address_library if
            self.address_library[n]["tagged"] is False
        )
        return keys_library

    # Set the tagged flag to True for visited kiosks so that they don't get visited multipel times
    def set_tagged_to_true(self, kiosk_id):
        for n in self.address_library:
            if self.address_library[n]["kiosk_id"] == kiosk_id:
                self.address_library[n]["tagged"] = True

    # Provide route details to the Driver object
    def populate_driver_route(self, driver_index, kiosk_id):
        for n in self.address_library:
            if self.address_library[n]["kiosk_id"] == kiosk_id:
                route = self.address_library[n]
                self.driver_dict[driver_index].route[kiosk_id] = route
                break

    # Check if all kiosks have been visited
    def check_if_complete(self):
        list_of_tagged = {}
        for n in range(len(self.address_library)):
            list_of_tagged[n] = self.address_library[n]["tagged"]
        if not all(list_of_tagged.values()):
            return False
        else:
            return True

    # Wrapper function to initiate drivers and generate routes for the objects
    def execute_path_mapping(self, number_of_drivers):
        self.initiate_drivers(number_of_drivers)
        self.set_driver_start_point()
        stop_number = 1
        while not self.check_if_complete():
            self.set_driver_next_point(stop_number)
            stop_number += 1
        for driver_index in self.driver_dict:
            for stop_number in self.driver_dict[driver_index].kiosk_ids:
                key = self.driver_dict[driver_index].kiosk_ids[stop_number]
                self.populate_driver_route(driver_index, key)
