# Time and Cost Solution

launch docker container according to the readme in
https://github.com/e-mission/em-public-dashboard

Here is an overview of the objective.

![Overview diagram](costtime.svg)

## How can I achieve choice model analysis with historical data?

The most crucial step in the process is finding and retrieving the
data. Quality data that is complete (spanning many years)
and accurate will allow for a more informed model.

## Time

We want to know the time it takes for an individual to use a particular mode
to get to a destination

### Transit

Transit is nuanced since there are many modes such as bus, rail, and tram.

#### Data Sources

GTFS (transit data standard) sources are varied, with some requiring monetary payment

| **Website Name**                            | **Dates**           | **URL**                                                                 | **Paid**                    | **Notes**                  |
|---------------------------------------------|---------------------|-------------------------------------------------------------------------|-----------------------------|----------------------------|
| Transitland                                 | 2016-Present        | [https://www.transit.land/feeds/f-9xj-rtd#versions](https://www.transit.land/feeds/f-9xj-rtd#versions) | Yes Unless Edu Academic Plan          | Does not have historical data without paid plan          |
| transitfeeds AKA OpenMobilityData           | 2015-Dec 2023       | [https://transitfeeds.com/p/rtd-denver/188?p=26](https://transitfeeds.com/p/rtd-denver/188?p=26) | No       | API Deprecated             |
| Scrape of transitfeeds AKA OpenMobilityData | Up to March 2021    | [https://raw.githubusercontent.com/interline-io/scrape-of-transitfeeds/refs/heads/master/json-scrape/feedVersionS3Urls.csv](https://raw.githubusercontent.com/interline-io/scrape-of-transitfeeds/refs/heads/master/json-scrape/feedVersionS3Urls.csv) | No                          |  Does not have recent data                 |
| Mobility Database                           | Feb 2024-Present    | [https://mobilitydatabase.org/feeds/mdb-178](https://mobilitydatabase.org/feeds/mdb-178) | No                          |  Does not have historical data            |

The CanBikeCO dataset does not go into 2024.

Thus, the most easy option was to scrape transitfeeds. This was done previously by someone else,
but that scrape was too old. Therefore, `scrape.ipynb` allows for an automated retrieval
of all GTFS data, for example, RTD Denver.

With this `scrape.ipynb` notebook, we are able to receive the astonishingly vast GTFS historical data from 2015 to the end of 2023. Datasets sometimes were released multiple times on a single
day, so it seems that every single change that the agencies made were recorded by transitfeeds.
Small changes such as the relocation of a singular stop would still reissue all of the data that remained unchanged, introducing redundancies. A form of version control, if implemented as a standard, would stop this.

#### GTFS Combination

It is not needed to have GTFS for every single day; it is unrealistic, as well, for computation
analysis to churn such significant amounts of data. We used only 1 GTFS file for every quarter
of the year. To distill this dataset, use the Jupyter cell marked `# Distill GTFS` in the
`scrape.ipynb`.

Then after distilling, download from 
https://github.com/OneBusAway/onebusaway-gtfs-modules/blob/master/docs/onebusaway-gtfs-merge-cli.md
and change the version accordingly within the jar filename in the following command.

```bash
java -jar -Xmx16G ~/Downloads/onebusaway-gtfs-merge-cli-3.2.4.jar denver/*.zip outputCombined.zip
```

#### OpenTripPlanner Launch

Ensure that docker is installed. This is not tested on Windows, so we assume you
have `make` available to run the Makefile. OTP does not work on Windows anyways.

The Makefile downloads the geofabrik pbf file for Colorado. This can be
parametrized, as can the `scrape.ipynb` notebook into a Python class/functions.

```bash
make
```

#### Transit Time Python API

Once OTP is loaded, verify that it works within the browser by going to
localhost:9999

The routing should work with dates several years in the past e.g. 2022
but some years in the data distilling cell skipped years such as 2015.

Navigate to the Jupyter cell prefaced with `# GraphQL Interface` to have
a Python API for getting transit times.


## Cost

### Transit

It is true that GTFS provides fare information.
However, agencies tend not to provide it. But NTD has all agencies' information.

Fare data for transit is taken from NTD. The average fare for each particular agency
is calculated for any arbitrary person- take, for instance, Gainesville, Florida.
Most riders are students who attend the University of Florida, and all of their
rides are free (this is the same for any faculty and staff).

There are still individuals who pay for fare. So Gainesville's average is $0.07
according to NTD.

To calculate average fare, use the e-mission-common function:

```python
# gainesville fl coordinates for the bus (thats why mode is MB)
# longitude, then latitude.
# google maps prefers latitude, then longitude.
# otherwise you will be in antarctica
intensities = await emcmft.get_transit_intensities(2022, [-82.328132, 29.626142], modes=['MB'])

# Access and print the average_fare
average_fare = intensities[0]['average_fare']
print("Average Fare:", average_fare)
# 0.07352028470412668
# wow, seven cents! $0.07
```

