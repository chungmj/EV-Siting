import pandas as pd
# Loading the data from the csv file to only obtain the state, longitude and latitude coordinates for the charging stations

df = pd.read_csv('Non-Tesla Level 2 (Apr 20 2022).csv', usecols=[
                 'State', 'Longitude', 'Latitude', 'EV DC Fast Count', 'EV Level2 EVSE Num', 'EV Level1 EVSE Num'])

# Filter the data to obtain the locations of Non-Tesla Level 2 chargers located in Virginia

# The vadf dataframe filiters all the data so it only includes the chargers located within the state of Virginia

vadf = df.loc[df.State == 'VA']

# The df81 dataframe filters the data for the EV chargers located within the horizontal stretch of I-81

df81 = vadf[vadf['Latitude'].between(36.6, 39.3)]
df81 = df81.sort_values('Latitude')

# The df81lvl1 dataframe filters the data inside the stretch of I-81 to include only the level 1 chargers and their locations

df81lvl1 = df81[df81['EV Level1 EVSE Num'] >= 1]
df81lvl1 = df81lvl1[['State', 'Longitude', 'Latitude', 'EV Level1 EVSE Num']]

# The df81lvl2 dataframe filters the data inside the stretch of I-81 to include only the level 2 chargers and their locations

df81lvl2 = df81[df81['EV Level2 EVSE Num'] >= 1]
df81lvl2 = df81lvl2[['State', 'Longitude', 'Latitude', 'EV Level2 EVSE Num']]

# The df81DC dataframe filters the data inside the stretch of I-81 to include only the DC fast chargers and their locations

df81DC = df81[df81['EV DC Fast Count'] >= 1]
df81DC = df81DC[['State', 'Longitude', 'Latitude', 'EV DC Fast Count']]
