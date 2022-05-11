**Data Analysis Final Project**

I-81 is an extensive transportation and shipping corridor that is frequented by commercial vehicles. This means there is a high amount of traffic along the interstate, which raises a concern for air quality. So, how do we begin to support Electric Commercial Vehicles along I-81 to promote the use of alternative fuel and the improvement of air quality? Our client, Virginia Clean Cities, is interested in knowing the truck stops along I-81 that can serve as a candidate for installing new Electric Vehicle (EV) Charging stations in order to extend the commercial electric vehicle corridor along I-81. To be considered a candidate, the truck stop must be within 50 miles away from another charging station, one mile away from an exit on I-81, and it must not currently have an EV Charging station.

The Data folder contains all the data provided to the group from Virginia Clean Cities, which are named alt_fuel_stations (Apr 25 2022).csv and VA Truck Stops.csv, edits were made manually to the VA Truck Stops.csv to included the addresses of all the truck stops located along I-81, to be used in the next python script for analysis.


**Required Installs before running**

pip install pandas

pip install folium

pip install geopy


**FindingCoordinates.py**

The first step in the final analysis was finding all the truck stops located off of I-81 and verifying that the truck stops were located within 1 mile of I-81, a filter was applied at the beginning of the code to only obtain the truck stops located off of I-81. By using the addresses of each of the truck stops, utilizing Nominatim, to find the GPS coordinates of each truck stops. Edits were made manually to the Updated_Truck_Stops.csv, the file that is created at the end of the python script, due to Nominatim not being able to find the GPS coordinates of all the truck stops. 


**Analysis**

The next step was filtering the EV charging data to include the chargers located closest to I-81 by setting a bound for longitude coordinates that cover the stretch of I-81
From the geopy results we decided to set a threshold for a distance of less than a mile for counting a truckstop with an EV charger
It was found that only two truck stops could be considered as truck stops with EV chargers from the set threshold
Using the two truck stops that were considered to have EV charging stations, another threshold was set of a distance less than 50 miles to identify potential candidates for implementing EV charging stations.

Upon running Analysis.py, the following files are generated: Truck_Stops_Without_EV_Chargers.csv, Truck_Stops_With_Charger.csv, Potential_Candidates.csv, DC_Fast_Chargers_81.csv, and Level2_Chargers_81.csv.

**PlottingPoints**

Lastly, from the analysis we used all the filtered and analyzed data to plot all GPS points on an interactive map to show all of the data.

**Combined.py**

This python file is the all three of the python files described above, Nominatim slows the run time of the code, so it was easier to seperate them to make edits to each part individually.
