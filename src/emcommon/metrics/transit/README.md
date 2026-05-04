how to run

run deprecated_transit.ipynb
then
run fares.py

# NTD Modes
['Demand Response' 'Heavy Rail' 'Commuter Bus' 'Bus' 'Bus Rapid Transit'
    'Commuter Rail' 'Vanpool' 'Light Rail' 'Hybrid Rail' 'Ferryboat'
    'Trolleybus' 'Streetcar Rail' 'Monorail/Automated Guideway'
    'Inclined Plane' 'Cable Car' 'Publico' 'Aerial Tramway' 'Alaska Railroad']


Regionalize the public transit cost using UACE Code
https://www.naturalearthdata.com/downloads/10m-cultural-vectors/
----relation with cost of living?


COst is just one feature in feature matrix
Can we pull safety 

Frequency of service at the time of day you want to take the trip.
get gtfs, is there a data source that publishes? where can we get the list

time of day. night may be undesirable

extend by year, parametrize the year


# NTD column names
['Agency', 'City', 'Fare Revenues per Unlinked Passenger Trip', 'State',
       'NTD ID', 'Organization Type', 'Reporter Type', 'Report Year',
       'UACE Code', 'UZA Name', 'Primary UZA Population', 'Agency VOMS',
       'Mode', 'Mode Name', 'TOS', 'Mode VOMS',
       'Fare Revenues per Unlinked Passenger Trip Questionable',
       'Fare Revenues per Total Operating Expense (Recovery Ratio)',
       'Fare Revenues per Total Operating Expense (Recovery Ratio) Questionable',
       'Cost per Hour', 'Cost per Hour Questionable',
       'Passengers per Vehicle Revenue Hour',
       'Passengers per Hour Questionable', 'Cost per Passenger',
       'Cost per Passenger Questionable', 'Cost per Passenger Mile',
       'Cost per Passenger Mile Questionable', 'Fare Revenues Earned',
       'Fare Revenues Earned Questionable', 'Total Operating Expenses',
       'Total Operating Expenses Questionable', 'Unlinked Passenger Trips',
       'Unlinked Passenger Trips Questionable', 'Vehicle Revenue Hours',
       'Vehicle Revenue Hours Questionable', 'Passenger Miles',
       'Passenger Miles Questionable', 'Vehicle Revenue Miles',
       'Vehicle Revenue Miles Questionable', 'Total Fare Revenue']



# chatgpt

1. can you go on Bing or Google and get the right link
2. Can you extract the right information from that link


# User - and gpt collaboration

1. go on google, get the correct link, and copy it, save it
  a. save these links
  b. wayback machine and traverse across years and download the past HTMLs and do the same process
2. download the html of that link, and give it to GPT (which is quite accurate.)

Is this realistic? How long does this take?

there are 400 bus agencies  coming from NTD


# TODO

see if fare price is in the GTFS.



# 9/16

if agenc doesnt have fare table, use fare published by nearby agency.
use average state value.

input: location
output: transit cost

we also want to input how frequent the transit is coming. the user is
likely dont want to wait around. 

How long is the next transit arriving? use that amount of time as model input.

consider paratransit, demand response mobility (an additional mode to
the preexisting ones that are GTFS standard)

----

build frequency on top of gtfs since we are going to be using it anyway
for fare. cost, time, frequency. frequency of non transit modes is infinite such as walk.

may want to use headway (0) meaning theres no wait time to just start walking. headway
for a bus might be 15 minutes. Just look at headway, which means the time between 
two subsequent opportunities to take the trip.

security of the resources. such as shared micromobility, if there is one
dock of scooters, and you go there and there are none, then you are stranded.

cost, time, availability (density or headway)
10/1


# Timeline

main intention is choice modelling
first, approximate.

9/16- i will complete the fare entry for each agency that there is, 
      and write a function that takes in coordinates (of a trip beginning), and returns 
      fare price

9/18- i already have the cost / pmt values for car, and walking, biking, etc.
      off of that, build a choice modelling using those values and the coordinate.

      very rudimentary

9/20- try opentripplanner for getting the transit time

# is there a latex class for suli paper

try to get 1st quartile of the fare 


# 9/18
move to scripts

extracting by urban area and list of codes



https://data.transportation.gov/Public-Transit/2022-NTD-Annual-Data-Service-by-Mode-and-Time-Peri/wwdp-t4re/about_data


# 9/20

Use emcommon/metrics/footprint/footprint_calculations, as a reference

Get the fare into the json
Figure out a plan how to read them similar to calculating footprint in above ^
Send NTD email to figure out headway, refer to paper 

rationalize their calculation https://www.sciencedirect.com/science/article/pii/S1077291X22002053


# 9/23

outline the proposal of-

- either combining cost with the intensities because the cost is part of the intensities
    line 95 prg metrics/footprint/transit.py-
    proposal is to just say intensities['fare'] = my_fare_variable
- OR making a duplicate function (maybe it is repeating ourselves) that just returns the fare according to UACE

the catch is, that multiple NTD IDs are attached to a single UACE Code. so, do we have to average out
all of the fares that are attached to that particular UACE?

This has Route Mileage and Start / End times of service for headway
https://data.transportation.gov/Public-Transit/2022-NTD-Annual-Data-Service-by-Mode-and-Time-Peri/wwdp-t4re/explore/query/SELECT%0A%20%20%60agency%60%2C%0A%20%20%60_5_digit_ntd_id%60%2C%0A%20%20%60reporter_type%60%2C%0A%20%20%60organization_type%60%2C%0A%20%20%60city%60%2C%0A%20%20%60state%60%2C%0A%20%20%60report_year%60%2C%0A%20%20%60agency_voms%60%2C%0A%20%20%60mode%60%2C%0A%20%20%60mode_name%60%2C%0A%20%20%60type_of_service%60%2C%0A%20%20%60mode_voms%60%2C%0A%20%20%60mode_voms_questionable%60%2C%0A%20%20%60primary_uza_code%60%2C%0A%20%20%60primary_uza_name%60%2C%0A%20%20%60primary_uza_area_sq_miles%60%2C%0A%20%20%60primary_uza_population%60%2C%0A%20%20%60service_area_sq_miles%60%2C%0A%20%20%60service_area_population%60%2C%0A%20%20%60time_period%60%2C%0A%20%20%60time_service_begins%60%2C%0A%20%20%60time_service_ends%60%2C%0A%20%20%60actual_vehicles_passenger_car_miles%60%2C%0A%20%20%60vehicle_miles_questionable%60%2C%0A%20%20%60actual_vehicles_passenger_car_revenue_miles%60%2C%0A%20%20%60vehicle_revenue_miles_questionable%60%2C%0A%20%20%60actual_vehicles_passenger_deadhead_miles%60%2C%0A%20%20%60deadhead_miles_questionable%60%2C%0A%20%20%60scheduled_vehicles_passenger_car_revenue_miles%60%2C%0A%20%20%60scheduled_revenue_miles_questionable%60%2C%0A%20%20%60actual_vehicles_passenger_car_hours%60%2C%0A%20%20%60vehicle_hours_questionable%60%2C%0A%20%20%60actual_vehicles_passenger_car_revenue_hours%60%2C%0A%20%20%60vehicle_revenue_hours_questionable%60%2C%0A%20%20%60actual_vehicles_passenger_car_deadhead_hours%60%2C%0A%20%20%60deadhead_hours_questionable%60%2C%0A%20%20%60charter_service_hours%60%2C%0A%20%20%60school_bus_hours%60%2C%0A%20%20%60trains_in_operation%60%2C%0A%20%20%60trains_in_operation_questionable%60%2C%0A%20%20%60train_miles%60%2C%0A%20%20%60train_miles_questionable%60%2C%0A%20%20%60train_revenue_miles%60%2C%0A%20%20%60train_revenue_miles_questionable%60%2C%0A%20%20%60train_deadhead_miles%60%2C%0A%20%20%60train_hours%60%2C%0A%20%20%60train_hours_questionable%60%2C%0A%20%20%60train_revenue_hours%60%2C%0A%20%20%60train_revenue_hours_questionable%60%2C%0A%20%20%60train_deadhead_hours%60%2C%0A%20%20%60unlinked_passenger_trips_upt%60%2C%0A%20%20%60unlinked_passenger_trips_questionable%60%2C%0A%20%20%60ada_upt%60%2C%0A%20%20%60sponsored_service_upt%60%2C%0A%20%20%60passenger_miles%60%2C%0A%20%20%60passenger_miles_questionable%60%2C%0A%20%20%60directional_route_miles%60%2C%0A%20%20%60directional_route_miles_questionable%60%2C%0A%20%20%60brt_non_statutory_mixed_traffic%60%2C%0A%20%20%60mixed_traffic_right_of_way%60%2C%0A%20%20%60days_of_service_operated%60%2C%0A%20%20%60days_not_operated_strikes%60%2C%0A%20%20%60days_not_operated_emergencies%60%2C%0A%20%20%60average_speed%60%2C%0A%20%20%60average_speed_questionable%60%2C%0A%20%20%60average_passenger_trip_length_aptl_%60%2C%0A%20%20%60aptl_questionable%60%2C%0A%20%20%60passengers_per_hour%60%2C%0A%20%20%60passengers_per_hour_questionable%60%0AORDER%20BY%20%60_5_digit_ntd_id%60%20ASC%20NULL%20LAST/page/filter


The difference between route mileage is like, a route to and back, is 20 miles. Whereas the vehicle 
mileage is all that is done over a particular time, such as taking the route over and over again, is 300 miles.
"Train Revenue Miles"
if there are only entries for non -train in the other column,
and only entries for train in "Train Revenue Miles", then we can merge them into a single
column called "Revenue Miles".

if train revenue miles is not zero and the otehr is not zero
why use the train revenue miles for Rail, when sometimes they have a Passenger Revenue Miles thats larger?

weigh the fare by the number of unlinked passenger trips

`get_transit_intensities` will help us test on data to see what the fare is for 
a particular set of coordinates.

# 9/24

The entries in the json are not differentiated by the mode,
there is an entry for each ntd id but there is redundant data
since the entry is not specific to that mode and TOS


There is One to Many routing r5 instead of OpenTripPlanner
(but this may be unnecessary)

first and foremost i will do the fare function 

outline the proposal of-

- either combining cost with the intensities because the cost is part of the intensities
    line 95 prg metrics/footprint/transit.py-
    proposal is to just say intensities['fare'] = my_fare_variable
- OR making a duplicate function (maybe it is repeating ourselves) that just returns the fare according to UACE

and then  i will look to see how i can solve the OTP issue,


# 9/27

use openmobility to get
historical gtfs because if you check denver
then it seems to only have recent months right now


# Fares

Saved link for MTA New York City Transit: https://new.mta.info/fares
Saved link for MTA New York City Transit: https://new.mta.info/fares
Saved link for New Jersey Transit Corporation: https://www.njtransit.com/fares
Saved link for New Jersey Transit Corporation: https://www.njtransit.com/fares
Saved link for Washington Metropolitan Area Transit Authority: https://www.wmata.com/fares/basic.cfm
^Cjfleisc1@jfleisc1-coolcomp:~/Desktop/nrel/e-mission-common/src/emcommon/metrics/transit$ 
jfleisc1@jfleisc1-coolcomp:~/Desktop/nrel/e-mission-common/src/emcommon/metrics/transit$ 
jfleisc1@jfleisc1-coolcomp:~/Desktop/nrel/e-mission-common/src/emcommon/metrics/transit$ python fares.py
^Cjfleisc1@jfleisc1-coolcomp:~/Desktop/nrel/e-mission-common/src/emcommon/metrics/transit$ python fares.py
Saved link for Los Angeles County Metropolitan Transportation Authority , dba: Metro: https://www.metro.net/riding/fares/
Saved link for New Jersey Transit Corporation: https://www.njtransit.com/fares
Saved link for Washington Metropolitan Area Transit Authority: https://www.wmata.com/fares/basic.cfm
Saved link for Los Angeles County Metropolitan Transportation Authority , dba: Metro: https://www.metro.net/riding/fares/
Saved link for Chicago Transit Authority: https://www.transitchicago.com/fares/
Saved link for King County Department of Metro Transit, dba: King County Metro: https://kingcounty.gov/en/dept/metro/fares-and-payment/prices
Saved link for Massachusetts Bay Transportation Authority: https://www.mbta.com/fares/bus-fares
Saved link for Southeastern Pennsylvania Transportation Authority: https://wwww.septa.org/fares/
Saved link for Maryland Transit Administration: https://www.mta.maryland.gov/regular-fares
Saved link for County of Miami-Dade , dba: Transportation & Public Work: https://tokentransit.com/agency/miamidadefl
Saved link for Metropolitan Transit Authority of Harris County, Texas: https://www.ridemetro.org/fares/all-about-fares
Saved link for Metro-North Commuter Railroad Company, dba: MTA Metro-North Railroad: bad
Saved link for MTA Bus Company: https://new.mta.info/fares
Saved link for Utah Transit Authority: https://m.rideuta.com/Fares-And-Passes/Current-Fares
Saved link for Pace - Suburban Bus Division: https://www.pacebus.com/fares
Saved link for Denver Regional Transportation District: https://www.rtd-denver.com/fares-passes/fares
Saved link for VIA Metropolitan Transit: https://www.viainfo.net/rates/
Saved link for Port Authority of Allegheny County: https://www.rideprt.org/fares-and-passes/fare-information/
Saved link for Metropolitan Atlanta Rapid Transit Authority: https://itsmarta.com/howtoride.aspx
Saved link for Dallas Area Rapid Transit: https://www.dart.org/fare/general-fares-and-overview/fares
Saved link for Tri-County Metropolitan Transportation District of Oregon: https://trimet.org/fares/index.htm
Saved link for City and County of San Francisco, dba: San Francisco Municipal Transportation Agency: https://www.sfmta.com/getting-around/muni/fares
Saved link for Orange County Transportation Authority: https://www.octa.net/getting-around/bus/oc-bus/fares-and-passes/overview/regular-fares/
Saved link for San Diego Metropolitan Transit System: https://www.sdmts.com/fares/fare-chart
Saved link for City and County of Honolulu, dba: City & County of Honolulu DTS: https://www.thebus.org/Fare/TheBusFares.asp
Saved link for Regional Public Transportation Authority, dba: Valley Metro: https://www.valleymetro.org/fares/pricing
Saved link for Metropolitan Council: bad
Saved link for Capital Metropolitan Transportation Authority, dba: Capital Metro: https://www.capmetro.org/fares-passes
Saved link for Regional Transportation Commission of Southern Nevada: https://www.rtcsnv.com/ways-to-travel/fares-passes/
Saved link for Central Florida Regional Transportation Authority: https://www.golynx.com/fares-passes/
Saved link for Alameda-Contra Costa Transit District: https://www.actransit.org/fares
Saved link for Delaware Transit Corporation: https://www.dartfirststate.com/RiderInfo/Fares/
Saved link for Central Pennsylvania Transportation Authority: bad
Saved link for Broward County Board of County Commissioners, dba: Broward County Transit Division: https://www.broward.org/BCT/Pages/FaresPasses.aspx
Saved link for Metro Transit: https://www.metrotransit.org/fares
Saved link for City of Phoenix Public Transit Department , dba: Valley Metro: https://www.valleymetro.org/fares/pricing
Saved link for Santa Clara Valley Transportation Authority: https://www.vta.org/go/fares
Saved link for Montachusett Regional Transit Authority: https://www.mrta.us/fare-passes/
Saved link for Snohomish County Public Transportation Benefit Area Corporation: https://www.communitytransit.org/fares-and-passes
Saved link for Bi-State Development Agency of the Missouri-Illinois Metropolitan District, dba: (St. Louis) Metro: https://www.metrostlouis.org/fares-and-passes/
Saved link for Regional Transportation Commission of Washoe County: https://rtcwashoe.com/public-transportation/fares-passes/
Saved link for Fort Worth Transportation Authority, dba: Trinity Metro: https://ridetrinitymetro.org/tickets/
Saved link for Pierce County Transportation Benefit Area Authority: https://www.piercetransit.org/PT-fares/
Saved link for The Greater Cleveland Regional Transit Authority: https://www.riderta.com/fares
Saved link for Milwaukee County, dba: Milwaukee County Transit System: https://www.ridemcts.com/fares
Saved link for Sacramento Regional Transit District, dba: Sacramento RT: https://www.sacrt.com/fares/
Saved link for Westchester County, dba: The Bee-Line System: https://transportation.westchestergov.com/bee-line/fares-and-metrocard
Saved link for Board of County Commissioners, Palm Beach County, dba: Palm Tran, Inc.: https://www.palmtran.org/cash-fare/
Saved link for Transportation District Commission of Hampton Roads, dba: Hampton Roads Transit: https://gohrt.com/fares/
Saved link for Capital District Transportation Authority: https://www.cdta.org/cdta-fares
Saved link for Southwest Ohio Regional Transit Authority, dba: Metro / Access: https://www.go-metro.com/fare-information
Saved link for County of Nassau, dba: Nassau Inter County Express: https://www.nicebus.com/Passenger-Information/Fares-Passes
Saved link for San Mateo County Transit District: https://www.samtrans.com/fares
Saved link for Foothill Transit: https://www.foothilltransit.org/fares-and-passes
Saved link for Transit Authority of River City: https://www.ridetarc.org/fare/fare-structure/
Saved link for Niagara Frontier Transportation Authority: https://metro.nfta.com/fares/fare-info
Saved link for City of Charlotte North Carolina, dba: Charlotte Area Transit System: https://www.charlottenc.gov/CATS/Fares-Passes
Saved link for Rhode Island Public Transit Authority: https://www.ripta.com/fares/
Saved link for Fairfax County, VA, dba: Fairfax Connector Bus System: https://www.fairfaxcounty.gov/connector/fares-and-policies
Saved link for Spokane Transit Authority: https://www.spokanetransit.com/fares-passes/fares-overview/
Saved link for Central Ohio Transit Authority: https://www.cota.com/riding-cota/fare-overview/
Saved link for Pinellas Suncoast Transit Authority: https://www.psta.net/how-to-ride/tickets-and-fares/
Saved link for Suburban Mobility Authority for Regional Transportation: https://www.smartbus.org/Fares
Saved link for Ben Franklin Transit: https://www.bft.org/fares/fares-information/
Saved link for City of Tucson: https://www.suntran.com/fares-passes/
Saved link for Victor Valley Transit Authority: https://vvta.org/fares/
Saved link for Suffolk County , dba: Dept of Public Works - Transportation Division: https://sctbus.org/System-Information
Saved link for Mass Transportation Authority: https://www.mtaflint.org/fares-passes/
Saved link for Regional Transit Service - Monroe County, dba: RTS Monroe (MB) and RTS Access (DR): https://www.myrts.com/Monroe/Enjoy-the-Ride-Guide/Fares-and-Passes
Saved link for Metropolitan Transit Authority: bad
Saved link for Greater Richmond Transit Company: https://ridegrtc.com/fares/and-rates/
Saved link for North County Transit District: https://gonctd.com/fares/fares-passes/
Saved link for Connecticut Department of Transportation - CTTRANSIT - Hartford Division: https://www.cttransit.com/fares
Saved link for Ann Arbor Area Transportation Authority: https://www.theride.org/fares-passes/fares
Saved link for Kitsap Transit: https://www.kitsaptransit.com/fares/fares
Saved link for Central New York Regional Transportation Authority, dba: New York Regional Transportation Authority: https://new.mta.info/fares
Saved link for Pioneer Valley Transit Authority: https://www.pvta.com/faresPassesBus.php
Saved link for Jacksonville Transportation Authority: https://www.jtafla.com/ride-jta/fares-passes/
Saved link for Blue Water Area Transportation Commission, dba: Blue Water Area Transit: https://bwbus.com/fares/
