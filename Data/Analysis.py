import pandas as pd
from geopy import distance



# Importing data from FindCoordinates to be used to calculate distances and finding potentential candidates for new EV truck stops
alltruckstops = pd.read_csv('Updated_Truck_Stops.csv')

# Loading in data for the EV level 2 chargers
altlvl2 = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols=[
                      'EV Level2 EVSE Num', 'Latitude', 'Longitude', 'Station Name', 'Street Address', 'City'])

# Loading in data for the EV DC fast chargers
altDC = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols=[
                    'EV DC Fast Count', 'Latitude', 'Longitude', 'Station Name', 'Street Address', 'City'])


# Filtering the EV level 2 chargers so it only includes points closer to I-81 and drops the values that don't have a charger
altlvl2['EV Level2 EVSE Num'] = altlvl2['EV Level2 EVSE Num']
altlvl2 = altlvl2.dropna()
altlvl2['Longitude'] = altlvl2['Longitude'].astype(float)
df81lvl2 = altlvl2[altlvl2['Longitude'].between(-82.2, -78.1)]


# Filtering the EV DC fast chargers so it only includes points closer to I-81
altDC['EV DC Fast Count'] = altDC['EV DC Fast Count']
altDC['Longitude'] = altDC['Longitude'].astype(float)
df81DC = altDC[altDC['Longitude'].between(-82.2, -78.1)]

# Sorts the values from the bottom of I-81 to the top of I-81
df81DC = df81DC.sort_values(['Longitude'])


# Convert latitude longitude coordinates from integers to floats

alltruckstops['latitude'] = alltruckstops['latitude'].astype(float)
alltruckstops['longitude'] = alltruckstops['longitude'].astype(float)

df81DC['Latitude'] = df81DC['Latitude'].astype(float)
df81DC['Longitude'] = df81DC['Longitude'].astype(float)

# Calculating distance between all truck stops and all ev chargers
df = pd.DataFrame()
dist = []
truckstop = []
evcharger = []
latit = []
longi = []
tstopwith = []
for idx, row in alltruckstops.iterrows():
    for index, rowdc in df81DC.iterrows():
        vectordist = distance.geodesic(
            (row['latitude'], row['longitude']), (rowdc['Latitude'], rowdc['Longitude'])).mi
        dist.append(vectordist)
        truckstop.append(row['Exit'])
        evcharger.append(rowdc['Station Name'])
        latit.append(row['latitude'])
        longi.append(row['longitude'])
        tstopwith.append(row['full_address'])
df = pd.DataFrame()
df['Exit'] = truckstop
df['Station_Name'] = evcharger
df['distance(mi)'] = dist
df['latitude'] = latit
df['longitude'] = longi
df['Truck Stop Address'] = tstopwith

# Find truck stops that are within 0.6 miles of an EV charger and add them into a list that represents
# trucks stops with a charging station
truckstopwithcharger = pd.DataFrame()
exit = []
station_name = []
mindist = []
lati = []
long = []
tstopaddress = []
for index, row in df.iterrows():
    if row['distance(mi)'] <= 0.6:
        exit.append(row['Exit'])
        station_name.append(row['Station_Name'])
        mindist.append(row['distance(mi)'])
        lati.append(row['latitude'])
        long.append(row['longitude'])
        tstopaddress.append(row['Truck Stop Address'])
    else:
        continue

# Putting all the data into a dataframe for the truckstop with a charger
truckstopwithcharger['Truck_Stop_Exit'] = exit
truckstopwithcharger['Charger'] = station_name
truckstopwithcharger['distancetocharger'] = mindist
truckstopwithcharger['latitude'] = lati
truckstopwithcharger['longitude'] = long
truckstopwithcharger['Truck Stop Address'] = tstopaddress

# Find distance between truck stops without a charger and truck stops with a charger.
# Then add the truck stops without a charger that are less than or equal to 50 miles away from a truck stop with
# a charger into a list that represents the potential candidates.
candidates = pd.DataFrame()
distance_stations = []
exit_for_stop = []
candidate_address = []
la = []
lo = []
for idx, row in truckstopwithcharger.iterrows():
    for index, rowt in alltruckstops.iterrows():
        station_dist = distance.geodesic(
            (row['latitude'], row['longitude']), (rowt['latitude'], rowt['longitude'])).mi
        if station_dist <= 50 and station_dist != 0:
            distance_stations.append(station_dist)
            exit_for_stop.append(row['Truck_Stop_Exit'])
            candidate_address.append(rowt['full_address'])
            la.append(rowt['latitude'])
            lo.append(rowt['longitude'])
        else:
            continue
# Putting all the data found for truckstops within 50 miles of the truckstop with a charger
candidates['Exit of Truck Stop with Charger'] = exit_for_stop
candidates['Address of Candidates'] = candidate_address
candidates['distance(mi)'] = distance_stations
candidates['latitude'] = la
candidates['longitude'] = lo


# Dropping all duplicated values before plotting points on the map
for idx, row in candidates.iterrows():
    for index, rowt in alltruckstops.iterrows():
        if rowt['full_address'] == row['Address of Candidates']:
            alltruckstops = alltruckstops.drop(index)
        else:
            continue

# After filtering through all the data, the filtered data can be saved as different csv files to be used later to plot all information
# on a map

# alltruckstops.to_csv('Truck_Stops_Without_EV_Chargers.csv', index=False)
candidates.to_csv('Potential_Candidates.csv', index=False)
# df81DC.to_csv('DC_Fast_Chargers_81.csv', index=False)
# df81lvl2.to_csv('Level2_Chargers_81.csv', index=False)
# truckstopwithcharger.to_csv('Truck_Stops_With_Charger.csv', index=False)
