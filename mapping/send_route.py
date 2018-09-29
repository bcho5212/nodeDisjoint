import pandas

from mapping.path_mapping import PathMapping


def prepare_routes():
    path_mapper = PathMapping()
    path_mapper.execute_path_mapping(number_of_drivers=2)
    return path_mapper


def send_routes(path_mapper: PathMapping):
    drivers = path_mapper.driver_dict
    for driver in drivers:
        d = pandas.DataFrame(driver)


if __name__ == "__main__":
    routes = prepare_routes()
    send_routes(routes)