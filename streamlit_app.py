import pandas as pd   # Para cargar y manipular los datasets
import numpy as np    # Para operaciones numéricas
import matplotlib.pyplot as plt   # Para gráficos básicos
import seaborn as sns             # Para gráficos más avanzados y estéticos
import streamlit as st

drivers = pd.read_csv("drivers_updated.csv")
fastest_laps = pd.read_csv("fastest_laps_updated.csv")
teams = pd.read_csv("teams_updated.csv")
winners = pd.read_csv("winners.csv")
drivers_per_country = drivers['Nationality'].value_counts()
drivers_per_country
colors = plt.cm.Paired.colors
plt.figure(figsize=(12,6))
plt.bar(drivers_per_country.index, drivers_per_country.values, color = colors)
plt.xticks(rotation = 90)
plt.xlabel("Nacionality")
plt.ylabel("Number of drivers")
plt.title("Drivers per country in F1")

st.pyplot(plt)