import pandas as pd
import time
import requests
import os
import zipfile
import gtfs_kit as gk


def retrieve_transit_fares_dataframe():
    link = "https://data.transportation.gov/api/views/ekg5-frzt/rows.csv?date=20231102&accessType=DOWNLOAD&bom=true&format=true"
    return pd.read_csv(link, thousands=',')


def retrieve_fare_revenue_dataframe():
    link = r"https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-04/2022%20Fare%20Revenue.xlsx"
    return pd.read_excel(link)


def calculate_cost_per_pmt(df, mode_category):
    """
    Calculate the cost per Passenger Mile Traveled ($/PMT) and the weighted/non-weighted
    averages of Fare Revenues per Unlinked Passenger Trip for a given mode category.

    This function filters the input DataFrame based on the specified mode category
    (e.g., 'bus', 'train', 'subway'), computes the total fare revenue and total 
    passenger miles for the relevant modes, and calculates the weighted cost per PMT.

    It also calculates both the weighted and non-weighted averages for Fare Revenues 
    per Unlinked Passenger Trip.

    Args:
        df (pd.DataFrame): The DataFrame containing fare and passenger data.
        mode_category (str): The mode category to filter by (e.g., 'bus', 'train', 'subway').

    Returns:
        pd.DataFrame: The filtered DataFrame containing data for the specified mode category.
    """
    
    # dictionary of mode categories and their corresponding modes
    # Please find all the possible modes in README.md
    mode_mapping = {
        'bus': ['Bus', 'Bus Rapid Transit'],
        'train': ['Heavy Rail', 'Light Rail', 'Commuter Rail'],
        'subway': ['Heavy Rail', 'Monorail/Automated Guideway'], # not sure if Heavy Rail is subway

    }

    # Get the list of relevant modes based on the mode category
    modes = mode_mapping.get(mode_category.lower(), [])

    if not modes:
        print(f"Invalid mode category '{mode_category}'. No matching modes found.")
        return

    # Filter the DataFrame based on the mode category
    filtered_df = df[df['Mode Name'].isin(modes)]

    # Drop rows where Passenger Miles are NaN or zero
    filtered_df = filtered_df.dropna(subset=['Passenger Miles'])
    filtered_df = filtered_df[filtered_df['Passenger Miles'] > 0]

    # Calculate total fare revenue (Fare per trip * Number of trips)
    filtered_df['Total Fare Revenue'] = filtered_df['Fare Revenues per Unlinked Passenger Trip'] * filtered_df['Unlinked Passenger Trips']

    # Calculate the total fare revenue and total passenger miles for the selected modes
    total_fare_revenue = filtered_df['Total Fare Revenue'].sum()
    total_passenger_miles = filtered_df['Passenger Miles'].sum()

    # Calculate the weighted average for Fare Revenues per Unlinked Passenger Trip
    if filtered_df['Unlinked Passenger Trips'].sum() > 0:
        weighted_avg = (filtered_df['Fare Revenues per Unlinked Passenger Trip'] * filtered_df['Unlinked Passenger Trips']).sum() / filtered_df['Unlinked Passenger Trips'].sum()
    else:
        weighted_avg = None

    # Calculate the non-weighted average for Fare Revenues per Unlinked Passenger Trip
    non_weighted_avg = filtered_df['Fare Revenues per Unlinked Passenger Trip'].mean()

    print(f"Mode category: {mode_category}")
    print("Total Fare Revenue:", total_fare_revenue)
    print("Total Passenger Miles:", total_passenger_miles)

    # Ensure that total_passenger_miles is not zero before calculating cost per PMT
    if total_passenger_miles > 0:
        cost_per_pmt = total_fare_revenue / total_passenger_miles
        print(f"Cost per Passenger Mile Traveled ($/PMT) for {mode_category}:", cost_per_pmt)
    else:
        print(f"No valid Passenger Miles data available to calculate cost per PMT for {mode_category}.")

    print("Weighted Average Fare Revenues per Unlinked Passenger Trip:", weighted_avg)
    print("Non-weighted Average Fare Revenues per Unlinked Passenger Trip:", non_weighted_avg)

    return filtered_df


def us_state_to_abbrev(backwards=False):
    state_dictionary = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }
    
    if backwards:
        # Switch keys and values
        return {v: k for k, v in state_dictionary.items()}
    return state_dictionary


def route_code_type():
    # Source: GTFS Standard https://gtfs.org/documentation/schedule/reference/#routestxt
    return {
        0: "Tram, Streetcar, Light rail",  # Any light rail or street level system within a metropolitan area.
        1: "Subway, Metro",  # Any underground rail system within a metropolitan area.
        2: "Rail",  # Used for intercity or long-distance travel.
        3: "Bus",  # Used for short- and long-distance bus routes.
        4: "Ferry",  # Used for short- and long-distance boat service.
        5: "Cable tram",  # Used for street-level rail cars where the cable runs beneath the vehicle (e.g., cable car in San Francisco).
        6: "Aerial lift, suspended cable car",  # Cable transport where cabins, cars, gondolas, or open chairs are suspended by means of one or more cables.
        7: "Funicular",  # Any rail system designed for steep inclines.
        11: "Trolleybus",  # Electric buses that draw power from overhead wires using poles.
        12: "Monorail"  # Railway in which the track consists of a single rail or a beam.
    }


def transitland_operators(api_key: str,
                state_codes: list):
    
    operators_url = "https://api.transit.land/api/v2/rest/operators"
    
    feed_data = []

    # get operator information, such as their agencies
    def process_operator(operator, state_code):
        agencies = operator.get('agencies', [])
        feeds = operator.get('feeds', [])
        
        for agency in agencies:
            agency_id = agency.get('agency_id')
            agency_name = agency.get('agency_name')
            places = agency.get('places', [])

            if places is None:
                places = []
            else:
                # make sure that, for each place in places,
                # the place['state'] == state_code
                if any(place.get('adm1_name') != us_state_to_abbrev()[state_code[-2:]] for place in places): 
                    print(f"Warning: place state does not match state code for agency {agency}")
                    continue

            # dictionary to store feed information
            for feed in feeds:
            
                # Record feed information
                feed_data.append({
                    'agency_id': agency_id,
                    'agency_name': agency_name,
                    'places': places,
                    'feed_id': feed.get('id'),
                    'feed_onestop_id': feed.get('onestop_id'),
                    'feed_spec': feed.get('spec'),
                    'state_code': state_code
                })

    # go state by state to get feeds
    def get_feeds_for_state(state_code):
        url = f"{operators_url}?adm1_iso={state_code}&api_key={api_key}"
        print(url)
        response = requests.get(url)
        
        if response.status_code == 200:
            operators = response.json().get('operators', [])
            
            for operator in operators:
                process_operator(operator, state_code)
        else:
            print(response.json())
            print(f"Failed to retrieve data for state: {state_code}")


    # use the function to get feeds for each state
    for state_code in state_codes:
        get_feeds_for_state(state_code)
        time.sleep(1)  # rate limit

    df_feeds = pd.DataFrame(feed_data)

    return df_feeds


def transitland_feeds(api_key: str,
                      df_feeds: pd.DataFrame):
    """
    Function to fetch and process feed information by onestop_id
    
    Args:
    
        api_key (str): The API key for the Transitland API.
        df_feeds (pd.DataFrame): The DataFrame containing feed information.
                                 Returned by transitland_operators function.
    """
    
    feed_url = "https://api.transit.land/api/v2/rest/feeds/"

    # Create a folder named gtfs_folder if it doesn't exist
    gtfs_folder = "gtfs_folder"
    if not os.path.exists(gtfs_folder):
        os.makedirs(gtfs_folder)

    # return the information from GTFS.
    def check_fare_and_agency(url_gtfs, feed_onestop_id):
        fare = None
        agency = 'Unknown Agency'
        agency_url = 'Unknown URL'
        fare_rider_categories = None
        rider_categories = None
        routes_info = []
        stops = pd.DataFrame()

        try:
            # define the path to save the ZIP file in gtfs_folder
            zip_file_path = os.path.join(gtfs_folder, f"{feed_onestop_id}.zip")

            # check if the ZIP file already exists to avoid redownloading
            if not os.path.exists(zip_file_path):
                response = requests.get(url_gtfs)
                if response.status_code != 200:
                    return fare, agency, agency_url, fare_rider_categories, rider_categories, routes_info, stops

                # save gtfs to folder
                with open(zip_file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Using cached GTFS for {feed_onestop_id}")

            # use gtfs_kit library to read standard GTFS feed data from the saved file
            feed = gk.read_feed(zip_file_path, dist_units='km')

            stops = feed.stops if feed.stops is not None else pd.DataFrame()


            try:
                fare_attributes = feed.fare_attributes
                fare = fare_attributes if not fare_attributes.empty else None
            except Exception as e:
                print(f"Error extracting fare: {e}")

            
            try:
                agency = feed.agency.iloc[0]['agency_name'] if not feed.agency.empty else 'Unknown Agency'
                agency_url = feed.agency.iloc[0]['agency_url'] if not feed.agency.empty else 'Unknown URL'
            except Exception as e:
                print(f"Error extracting agency info: {e}")

            # get routes
            if feed.get_routes() is not None:
                routes_df = feed.get_routes()
                routes_info = routes_df.to_dict()  # store route information as a list of dictionaries
                

            # Check for fare_rider_categories.txt and rider_categories.txt manually
            # this could be a contribution to gtfs_kit
            try:
                with zipfile.ZipFile(zip_file_path) as zip_content:
                    if 'fare_rider_categories.txt' in zip_content.namelist():
                        fare_rider_categories = pd.read_csv(zip_content.open('fare_rider_categories.txt'))

                    if 'rider_categories.txt' in zip_content.namelist():
                        rider_categories = pd.read_csv(zip_content.open('rider_categories.txt'))
            except Exception as e:
                print(f"Error extracting rider categories: {e}")

            return fare, agency, agency_url, fare_rider_categories, rider_categories, routes_info, stops

        except Exception as e:
            print(f"Error processing feed: {e}")
            return fare, agency, agency_url, fare_rider_categories, rider_categories, routes_info, stops


    # get feed information for each feed_onestop_id
    def process_feed_by_onestop_id(feed_onestop_id, places, state_code):
        
        # use the feed_onestop_id to get feed details from the API
        url = f"{feed_url}{feed_onestop_id}?api_key={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            feed_info = response.json()
            
            url_gtfs = feed_info['feeds'][0]['urls'].get('static_current')
            print(f"Processing GTFS for {feed_onestop_id}: {url_gtfs}")
            stops = None

            # if url_gtfs and (country == 'United States of America'):
            if url_gtfs:

                fare, agency_name, agency_url, fare_rider_categories, rider_categories, routes_info, stops \
                    = check_fare_and_agency(url_gtfs, feed_onestop_id)
                print(f"Processed GTFS for {feed_onestop_id}: {routes_info} {fare}, {agency_name}, {agency_url}")
                return {
                    'feed_onestop_id': feed_onestop_id,
                    'agency_name': agency_name,
                    'agency_url': agency_url,
                    'url_gtfs': url_gtfs,
                    'fare': fare,
                    'fare_rider_categories': fare_rider_categories,
                    'rider_categories': rider_categories,
                    'stops': stops,
                    'routes_info': routes_info,
                    'places': places,
                    'state_code': state_code
                }
                
            else:
                return {
                    'feed_onestop_id': feed_onestop_id,
                    'agency_name': 'Unknown Agency',
                    'agency_url': 'Unknown URL',
                    'url_gtfs': url_gtfs,
                    'fare': None,
                    'fare_rider_categories': None,
                    'rider_categories': None,
                    'stops': stops,
                    'routes_info': None,  # If no routes info is available
                    'places': places,
                    'state_code': state_code
                }
        else:
            print(f"Failed to retrieve feed details for {feed_onestop_id}")
            return None


    # go through each feed_onestop_id to get feed details
    def gather_fare_info_from_df(df_feeds):
        feed_data = []
        
        # Get the feed data corresponding to each feed.
        for _, row in df_feeds.iterrows():
            feed_onestop_id = row['feed_onestop_id']
            places = row['places']
            state_code = row['state_code']
            
            feed_info = process_feed_by_onestop_id(feed_onestop_id, places, state_code)
            
            if feed_info:
                feed_data.append(feed_info)
            
            # rate limit
            time.sleep(1)
        
        return pd.DataFrame(feed_data)

    # use the feeds to get fare info.
    df_feeds_with_fare_info = gather_fare_info_from_df(df_feeds)

    df_feeds_with_fare_info.to_csv('updated_feed_fare_data.csv', index=False)

    # convert route_type to human readable format
    for index, row in df_feeds_with_fare_info.iterrows():
        if row['routes_info'] is not None and len(row['routes_info']) > 0:
            # pprint(row['routes_info'])
            # make a set out of the dictionary row['routes_info']['route_type'] values
            
            route_types = set([value for value in row['routes_info']['route_type'].values()])
            print(route_types)
            if len(route_types) > 1:
                row['route_type_human_readable'] = [route_code_type()[route_type] for route_type in list(route_types)]
                print(row['route_type_human_readable'], row['agency_name'])
            elif len(route_types) == 1:
                row['route_type_human_readable'] = route_code_type()[list(route_types)[0]]
                print(row['route_type_human_readable'], row['agency_name'])
                
        
    return df_feeds_with_fare_info
