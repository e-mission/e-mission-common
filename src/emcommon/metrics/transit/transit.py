import pandas as pd


def retrieve_transit_fares_dataframe():
    link = "https://data.transportation.gov/api/views/ekg5-frzt/rows.csv?date=20231102&accessType=DOWNLOAD&bom=true&format=true"
    return pd.read_csv(link, thousands=',')


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
        None: Prints the cost per Passenger Mile Traveled ($/PMT) for the selected mode category,
              as well as the weighted and non-weighted average fare revenues.
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

