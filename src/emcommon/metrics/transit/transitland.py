from pprint import pprint
import gtfs_kit as gk
import requests


# Save the original requests.get and requests.head functions
original_get = requests.get
original_head = requests.head

# Define a new version for requests.get and requests.head that always uses verify=False
def new_get(*args, **kwargs):
    kwargs['verify'] = False
    return original_get(*args, **kwargs)

def new_head(*args, **kwargs):
    kwargs['verify'] = False
    return original_head(*args, **kwargs)

# Monkey-patch both requests.get and requests.head
requests.get = new_get
requests.head = new_head

# Now both requests.get and requests.head will use verify=False automatically

# Any subsequent requests.get calls will use verify=False by default

# Define the API key
api_key = "i dont know what the api key is :)"

# Construct the URL with the API key as a query parameter
url = f"https://api.transit.land/api/v2/rest/feeds?api_key={api_key}"

# Make a GET request to the URL
print(url)
response = requests.get(url, verify=False)

# Print the response
url_gtfs = response.json()['feeds'][0]['urls']['static_current']
print(url_gtfs)
# print all values availabe in feeds of 0.
pprint(response.json()['feeds'][0].keys())
 
# but only thekeeys not the values.
import sys; sys.exit(0)

# Download and read the GTFS feed
feed = gk.read_feed(url_gtfs, dist_units='km')

# Get fare attributes (fare prices, currency, etc.)
fare_attributes = feed.fare_attributes
pprint(fare_attributes.head())

# Get fare rules (conditions for applying certain fares, like route or zone)
fare_rules = feed.fare_rules
print(fare_rules)

# Get fare attributes (price, currency)
fare_attributes = feed.fare_attributes[['fare_id', 'price', 'currency_type']]
pprint(fare_attributes.head())

