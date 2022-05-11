**Data Analysis Final Project**

In the Data folder it contains all the data provided to the group from Virginia Clean Cities, which are named alt_fuel_stations (Apr 25 2022).csv and VA Truck Stops.csv, edits were made manually to the VA Truck Stops.csv to included the addresses of all the truck stops located along I-81, to be used in the next python script for analysis.

**FindingCoordinates.py**

The first step in the final analysis was finding all the truck stops located off of I-81 and verifying that the truck stops were located within 1 mile of I-81, a filter was applied at the beginning of the code to only obtain the truck stops located off of I-81. By using the addresses of each of the truck stops, utilizing Nominatim, to find the GPS coordinates of each truck stops. Edits were made manually to the Updated_Truck_Stops.csv, the file that is created at the end of the python script, due to Nominatim not being able to find the GPS coordinates of all the truck stops. 


**Analyzing.py**

The next step was filtering the EV charging data to include the chargers located closest to I-81 by setting a bound for longitude coordinates that cover the stretch of I-81
From the geopy results we decided to set a threshold for a distance of less than a mile for counting a truckstop with an EV charger
It was found that only two truck stops could be considered as truck stops with EV chargers from the set threshold
Using the two truck stops that were considered to have EV charging stations, another threshold was set of a distance less than 50 miles to identify potential candidates for implementing EV charging stations

**PlottingPoints**

Lastly, from the analysis we used all the filtered and analyzed data to plot all GPS points on an interactive map to show all of the data

**Combined.py**

This python file is the all three of the python files described above, Nominatim slows the run time of the code, so it was easier to seperate them to make edits to each part individually.
