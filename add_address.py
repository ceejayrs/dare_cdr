import pandas
from geopy.geocoders import ArcGIS
import csv

nom = ArcGIS()

df = pandas.read_csv("ncr.csv")

df["address"] = df["name"] + "," + df["submun"] + "," + df["city"] + "," + df["province"]

df["coordinates"] = df["address"].apply(nom.geocode)

