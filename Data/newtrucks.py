import pandas as pd

# Loading the data from the csv for truck stops in Virginia
dftruck = pd.read_csv('VA Truck Stops.csv')

# filtering the data to only include the truck stops located off of I-81
dftruck = dftruck[dftruck['Highway'].str.contains("81")]

print(dftruck)