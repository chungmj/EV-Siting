import webbrowser
import pandas as pd
import folium

# Loading in all the data that was filtered and analyzed from the FilteringData python code
alltruckstops = pd.read_csv('Truck_Stops_Without_EV_Chargers.csv')
candidates = pd.read_csv('Potential_Candidates.csv')
df81DC = pd.read_csv('DC_Fast_Chargers_81.csv')
df81lvl2 = pd.read_csv('Level2_Chargers_81.csv')
truckstopwithcharger = pd.read_csv('Truck_Stops_With_Charger.csv')

# Creating the map and plotting all the GPS coordinates on the map
map = folium.Map(location=[37.806507, -
                 79.389342], zoom_start=8)

# Creating groups for a legend to be shown on the map
truckstops = folium.FeatureGroup(name='Truck Stops without EV charger (red)')
evtruckstop = folium.FeatureGroup(name='Truck Stop with EV charger (orange)')
dcchargers = folium.FeatureGroup(name='EV DC Fast Chargers (green)')
possibletruckstops = folium.FeatureGroup(
    name='Possible new locations for EV truck stops (blue)')
lvl2chargers = folium.FeatureGroup(name='Level 2 Chargers (purple)')

# Plotting points of all the truck stops located along I-81
for index, row in alltruckstops.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), icon=folium.Icon(
        color='red'), popup=row['full_address']).add_to(truckstops)
    truckstops.add_to(map)

# Plotting all points for the potential candidates that are within 50 miles of the truck stop with a EV charger
for index, row in candidates.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), popup=str(int(row['distance(mi)'])) + 'miles from truck stop exit:' + str(
        row['Exit of Truck Stop with Charger']) + ' with a charger ' + '<br>' + 'Address of Candidate: ' + row['Address of Candidates']).add_to(possibletruckstops)
    possibletruckstops.add_to(map)

# Plotting all the points for the EV DC Fast chargers located near I-81
for index, row in df81DC.iterrows():
    folium.Marker(location=(row['Latitude'], row['Longitude']), icon=folium.Icon(
        color='green'), popup='Number of DC Fast Chargers: ' + str(int(row['EV DC Fast Count']))).add_to(dcchargers)
    dcchargers.add_to(map)

# Plotting all the points for the EV level 2 chargers near I-81
for index, row in df81lvl2.iterrows():
    folium.Marker(location=(row['Latitude'], row['Longitude']), icon=folium.Icon(
        color='purple'), popup='Number of level 2 chargers =' + str(int(row['EV Level2 EVSE Num']))).add_to(lvl2chargers)
    lvl2chargers.add_to(map)

# Plotting the truck stop with an EV charger
for index, row in truckstopwithcharger.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude']), icon=folium.Icon(
        color='orange'), popup='EV Station name: ' + str(row['Charger']) + '<br>' + ' Truck stop address: ' + str(row['Truck Stop Address'])).add_to(evtruckstop)
    evtruckstop.add_to(map)

# Adding a legend to the map which can be turned on and off
folium.map.LayerControl('topleft', collapsed=False).add_to(map)

# Saving the map and opening the map so it can be visible
map.save('map1.html')
webbrowser.open('map1.html')
