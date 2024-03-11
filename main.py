# Partículas Respiráveis (<2,5µm)(µg/m3)
# PM 2,5 µg/m3

# main objetive is to import all the data from the excel files and plot the data of PM2.5 in a graph
# the data is located in the folder "data" and the files are in the folder "name_of_the_station"
# the data are named as "name_of_the_station_year.xlsx", for example "Castata_2019.xlsx". from 2009 to 2022
# the data is in the column "PM 2,5" or "Partículas Respiráveis (<2,5µm)(µg/m3)" and the time is in the column "Data" and "Hora"
# the data is in the format "dd/mm/yyyy" and "hh:mm"

import os
import pandas as pd
import matplotlib.pyplot as plt

# Set the path to the main data folder
main_folder = "data"

# List all folders (stations) in the main folder
station_folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

# Iterate through each station folder
for station_folder in station_folders:
    # Create an empty DataFrame to store the combined data for the current station
    combined_data = pd.DataFrame()

    # List all files in the current station folder
    files = [f for f in os.listdir(os.path.join(main_folder, station_folder)) if f.endswith(".xlsx")]

    # Iterate through each file
    for file in files:
        # Extract the year from the file name
        year = int(file.split("_")[1].split(".")[0])

        # Construct the full path to the Excel file
        file_path = os.path.join(main_folder, station_folder, file)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Combine the current year's data with the previous years' data
        combined_data = pd.concat([combined_data, df])

        # select the column for PM2.5 (use either "PM 2,5" or "Partículas Respiráveis (<2,5µm)(µg/m3)")
        pm25_column = df["PM 2,5"] if "PM 2,5" in df.columns else df["Partículas Respiráveis (<2,5µm)(µg/m3)"]

        combined_data = pd.concat([combined_data, pm25_column], axis=1)

    # Combine date and time columns into a single datetime column
    combined_data['DateTime'] = pd.to_datetime(combined_data['Data'] + ' ' + combined_data['Hora'], format='%d/%m/%Y %H:%M')

    # Plot the data for PM2.5
    plt.figure(figsize=(10, 6))
    plt.plot(combined_data['DateTime'], combined_data['PM 2,5'], label=f"{station_folder} PM2.5")

    # Customize the plot as needed
    plt.title("PM2.5 Data Over Time")
    plt.xlabel("Date and Time")
    plt.ylabel("PM2.5 (µg/m3)")
    plt.legend()
    plt.grid(True)
    plt.show()
