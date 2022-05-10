from IPython.display import display
import webbrowser
import pandas as pd
import folium
from geopy import distance
from geopy.geocoders import Nominatim


# Loading the data from the csv for truck stops in Virginia
dftruck = pd.read_csv('VA Truck Stops.csv')

# filtering the data to only include the truck stops located off of I-81
dftruck = dftruck[dftruck['Highway'].str.contains("81")]

# Removes the decimal place that is part of the zip code
dftruck['ZIP'] = dftruck['ZIP'].astype(int)

# Makes the zipcode into a string so it can be used later in writing the full address of the truck stop
dftruck['ZIP'] = dftruck['ZIP'].astype(str)


# Adds a column that contains the full address of the truck stop
dftruck['full_address'] = dftruck.Street_Address + ',' + \
    dftruck.City + ',' + dftruck.State + ',' + dftruck.ZIP

# Removes the qutation marks that the full address has
dftruck['full_address'] = dftruck.full_address.replace('""', '')

# sets up the geolocator so it can be used to read the addresses of the truck stops and coverts them to gps coordinates
geolocator = Nominatim(user_agent="Python")

# Empty lists for the latitude and longitude coordinates of each address
lat = []
long = []

# This function loops through the truck stops addresses and checks if the address has a GPS coordinate, if a GPS coordinate is not found
# it returns None for the latitude and longitude, if it is found it returns the latitude and longitude
for row in dftruck['full_address']:
    location = geolocator.geocode(row)
    if location is None:
        latitude = None
        longitude = None
    else:
        latitude = location.latitude
        longitude = location.longitude
    lat.append(latitude)
    long.append(longitude)

# adds a longitude and latitude column to the data frame
dftruck['latitude'] = lat
dftruck['longitude'] = long

# This was used to save the filtered data as a csv file, so the truck stops that didn't have latitude and longitude coordinates
# could be manually added to include them

# dftruck.to_csv('Updatedlist.csv', index=False)

# Has all the points found in the above function and for every none type found, had to make edits to manually add the latitude and longitude
alltruckstops = pd.read_csv('Truck_Stop_Points.csv')

# Loading in data for the EV level 2 chargers
altlvl2 = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols=[
                      'EV Level2 EVSE Num', 'Latitude', 'Longitude'])

# Loading in data for the EV DC fast chargers
altDC = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols=[
                    'EV DC Fast Count', 'Latitude', 'Longitude', 'Station Name'])


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

for idx, row in alltruckstops.iterrows():
    for index, rowdc in df81DC.iterrows():
        vectordist = distance.geodesic(
            (row['latitude'], row['longitude']), (rowdc['Latitude'], rowdc['Longitude'])).mi
        dist.append(vectordist)
        truckstop.append(row['Exit'])
        evcharger.append(rowdc['Station Name'])
        latit.append(row['latitude'])
        longi.append(row['longitude'])
df = pd.DataFrame()
df['Exit'] = truckstop
df['Station_Name'] = evcharger
df['distance(mi)'] = dist
df['latitude'] = latit
df['longitude'] = longi


# Find truck stops that are within 1 mile of an EV charger and add them into a list that represents
# trucks stops with a charging station
truckstopwithcharger = pd.DataFrame()
exit = []
station_name = []
mindist = []
lati = []
long = []
for index, row in df.iterrows():
    if row['distance(mi)'] <= 0.6:
        exit.append(row['Exit'])
        station_name.append(row['Station_Name'])
        mindist.append(row['distance(mi)'])
        lati.append(row['latitude'])
        long.append(row['longitude'])
    else:
        continue
# Putting all the data into a dataframe for the truckstop with a charger
truckstopwithcharger['Truck_Stop_Exit'] = exit
truckstopwithcharger['Charger'] = station_name
truckstopwithcharger['distancetocharger'] = mindist
truckstopwithcharger['latitude'] = lati
truckstopwithcharger['longitude'] = long

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
candidates['Tstop Charger'] = exit_for_stop
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

# Creating the map and plotting all the GPS coordinates on the map
map = folium.Map(location=[37.806507, -
                 79.389342], zoom_start=8)

# Creating groups for a legend to be shown on the map
truckstops = folium.FeatureGroup(name= 'Truck Stops without EV charger (red)')
evtruckstop = folium.FeatureGroup(name= 'Truck Stop with EV charger (orange)')
dcchargers = folium.FeatureGroup(name= 'EV DC Fast Chargers (green)')
possibletruckstops = folium.FeatureGroup(name= 'Possible new locations for EV truck stops (blue)')
lvl2chargers = folium.FeatureGroup(name= 'Level 2 Chargers (purple)')

# Plotting points of all the truck stops located along I-81
for index, row in alltruckstops.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), icon=folium.Icon(
        color='red'), popup=row['full_address']).add_to(truckstops)
    truckstops.add_to(map)

# Plotting all points for the potential candidates that are within 50 miles of the truck stop with a EV charger
for index, row in candidates.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), popup=str(int(row['distance(mi)'])) + ' miles from truck stop with a charger').add_to(possibletruckstops)
    possibletruckstops.add_to(map)

# Plotting all the points for the EV DC Fast chargers located near I-81
for index, row in df81DC.iterrows():
    folium.Marker(location=(row['Latitude'], row['Longitude']), icon=folium.Icon(
        color='green'), popup='Number of DC Fast Chargers =' + str(row['EV DC Fast Count'])).add_to(dcchargers)
    dcchargers.add_to(map)

# Plotting all the points for the EV level 2 chargers near I-81
for index, row in df81lvl2.iterrows():
    folium.Marker(location=(row['Latitude'], row['Longitude']), icon=folium.Icon(
        color='purple'), popup='Number of level 2 chargers =' + str(row['EV Level2 EVSE Num'])).add_to(lvl2chargers)
    lvl2chargers.add_to(map)

# Plotting the truck stop with an EV charger
for index, row in truckstopwithcharger.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), icon=folium.Icon(
        color='orange'), popup=row['Charger']).add_to(evtruckstop)
    evtruckstop.add_to(map)

# Adding a legend to the map which can be turned on and off
folium.map.LayerControl('topleft', collapsed= False).add_to(map)

# Saving the map and opening the map so it can be visible
map.save('map1.html')
webbrowser.open('map1.html')