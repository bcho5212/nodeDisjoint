class Driver:
    def __init__(self, driver_rank, driver_phone):
        self.driver_rank = driver_rank
        self.driver_phone = driver_phone
        self.kiosk_ids = dict()
        self.route = dict()
