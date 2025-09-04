import os
import random
import googlemaps
import pandas as pd
from dotenv import load_dotenv

seed = 67
random.seed(seed)

load_dotenv()
api_key = os.getenv('api_key')
maps = googlemaps.Client(key=api_key)

data = pd.read_csv("UK_Cities.csv")
data = data[["City", "Latitude","Longitude"]]

new_data = pd.DataFrame({"Num Cities":[], "Start":[], "End":[], "Route":[], "Distance":[]})

sample = data["City"].sample(n=5, random_state=seed).tolist()

start = 3
end = 49

for i in range(end-start):
    sample = data["City"].sample(n=i+start, random_state=seed).tolist()

    for city in sample:
        row = data.index[data["City"]==city].item()
        start_coor = (data.loc[row, "Latitude"], data.loc[row, "Longitude"])
        other_cities = [o for o in sample if o != city]

        for dest in other_cities:
            route = city+"-"+dest

            row = data.index[data["City"]==dest].item()
            dest_coor = (data.loc[row, "Latitude"], data.loc[row, "Longitude"])

            try:
                dist = new_data[((new_data["Start"]==city) & (new_data["End"]==dest)) | ((new_data["End"]==city) & (new_data["Start"]==dest))]["Distance"].values[0]
            except:
                matrix = maps.distance_matrix(start_coor, dest_coor,  mode="driving", units="metric")
                dist = matrix['rows'][0]['elements'][0]['distance']['text']

            new_row = pd.DataFrame([[i+start, city, dest, route, dist]], columns=new_data.columns)
            new_data = pd.concat([new_data, new_row])  

            print(f"Cities: {i+start}, Start: {city}, Dist {dist}")

print(new_data)

new_data.to_csv("data.csv", index=False)