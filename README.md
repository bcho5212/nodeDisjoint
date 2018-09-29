# nodeDisjoint

This python project will intake the coordinates file that was provided and determine the most efficient paths between
kiosks for a specified number of drivers starting from the starting coordinates that were provided.

- (Mac) Steps to run:
    - Open Terminal and activate the virtual environment within the nodeDisjoint project:
        source ./venv/bin/activate
    - With the environment activated, run the send_route.py script:
        python ./send_route.py
    - You'll be prompted for the following:
        - "Path to file: "
            -> This input just needs the full path to the coordinates file
        - "Number of drivers: "
            -> This input requires you to put in the number of drivers that the python script will generate
            routes for
    - The project will then run the modules that process the file and generate the route, then outputs a file at:
        - "./nodeDisjoint/test/output/..."

- Additional notes:
    - Processing Steps:
        1) Takes user input file and generates a data frame
        2) Adds some additional elements to each row in the data frame for later use:
            kiosk_id
            tagged
        3) Generates a dictionary of Driver objects to add stops and routes to
        4) Starts by calculating the shortest distance to the start point for all kiosks and sets that as the starting
        point
        5) Loops through the rest of the kiosks, using the previous kiosk's coordinates and calculates the shortest
        distance
        6) Tags kiosks as "tagged = True" after each loop to prevent drivers from visiting the same kiosk multiple times
        7) Populates the Driver objects with their respective routes
        8) Outputs the route to a csv file
    - There were some kiosks tied to duplicated coordinates:
        name
        Chicago Midway Airport - Ticketing Employee Lounge
        Good Samaritan Hospital
        Medical College of Wisconsin
        Peggy Notebaert Nature Museum
        O'Hare Terminal 2 - Gate F6
        Good Shepherd Hospital
        Allstate HQ (Tenants Only)
        MillerCoors HQ
        100 E Wisconsin
        Moraine Valley Community College: Police Academy- Building B
        -> I left these in the coordinates but it does cause the results to look a little off as there is a name/address
        tied to WI that shows up as one of the earlier routes

    - To-Do's (Features / Improvements I would have liked to add):
        - Exception Handling:
            - The file doesn't exist
            - The file schema is completely wrong (i.e. it is not a coordinates file)
            - The file might require additional parsing / parameters to be added to the pandas functions
            - "Number of drivers" input is not an integer
            - "Number of drivers" input is negative
            - "Number of drivers" input is larger than the number of kiosks
        - Additional Features:
            - Googlemaps API integration
                - Loop through the coordinates and feed them into Google maps, adding them as destinations
            - SMS Message / Email
                - Get a link to the route mapped by Google maps and send it to drivers