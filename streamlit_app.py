import pandas as pd   # Para cargar y manipular los datasets
import numpy as np    # Para operaciones numéricas
import matplotlib.pyplot as plt   # Para gráficos básicos
import seaborn as sns             # Para gráficos más avanzados y estéticos
import streamlit as st
import unicodedata

drivers = pd.read_csv("drivers.csv", index_col=None)
fastest_laps = pd.read_csv("fastest_laps_.csv")
teams = pd.read_csv("teams.csv")
winners = pd.read_csv("winners.csv")
drivers_24 = pd.read_csv("drivers_2024_final.csv")
fastest_laps_24 = pd.read_csv("fastest_laps_2024.csv")
teams_24 = pd.read_csv("teams_2024_fixed.csv")

drivers_24

drivers_completed = pd.concat([drivers, drivers_24])

fastest_laps_completed = pd.concat([fastest_laps, fastest_laps_24])


def drivers_correction(drivers):
    # Convertir "NaN" string a valores NaN reales
    drivers.replace("NaN", pd.NA, inplace=True)
    drivers.replace("Nan", pd.NA, inplace=True)  # En caso de inconsistencia con "Nan"

    # Rellenar valores NaN con los datos de respaldo
    drivers["Pos"].fillna(drivers["Position"], inplace=True)
    drivers["Car"].fillna(drivers["Team"], inplace=True)
    
    # Convertir columnas numéricas correctamente
    drivers["PTS"].fillna(drivers["Points"], inplace= True)
    drivers["year"].fillna(drivers["Year"], inplace = True)
    
    return drivers

drivers_corrected = drivers_correction(drivers_completed)

drivers_corrected.drop(["Position", "Team", "Points", "Year"], axis=1, inplace= True)

def laps_correction(fastest_laps):
    # Convertir "NaN" string a valores NaN reales
    fastest_laps.replace("NaN", pd.NA, inplace=True)
    fastest_laps.replace("Nan", pd.NA, inplace=True)  # En caso de inconsistencia con "Nan"

    # Rellenar valores NaN con los datos de respaldo
    fastest_laps["year"].fillna(fastest_laps["Year"], inplace=True)

    
    return fastest_laps

fastest_laps_corrected = laps_correction(fastest_laps_completed)

fastest_laps_corrected.drop(["Year"], axis=1, inplace = True)

teams_completed = pd.concat([teams, teams_24])

def teams_correction(teams):
    # Convertir "NaN" string a valores NaN reales
    teams.replace("NaN", pd.NA, inplace=True)
    teams.replace("Nan", pd.NA, inplace=True)  # En caso de inconsistencia con "Nan"

    # Rellenar valores NaN con los datos de respaldo
    teams["year"].fillna(teams["Year"], inplace=True)
    teams["PTS"].fillna(teams["Points"], inplace= True)

    
    return teams

teams_corrected = teams_correction(teams_completed)

teams_corrected.drop(["Year"], axis= 1, inplace= True)

# Diccionario de equipos
equipos_normalizados = {
    "McLaren": ["McLaren", "McLaren Ford", "McLaren BRM", "McLaren TAG", "McLaren Honda", "McLaren Mercedes", "McLaren Renault", "McLaren Peugeot"],
    "Ferrari": ["Ferrari", "Minardi Ferrari", "Dallara Ferrari", "Sauber Ferrari", "Alfa Romeo Ferrari", "Kick Sauber Ferrari"],
    "Red Bull": ["Red Bull", "RBR Cosworth", "Red Bull Renault", "RBR Ferrari", "Red Bull Racing Renault", "Red Bull Racing TAG Heuer", "Red Bull Racing Honda", "Red Bull Racing RBPT", "Red Bull Racing Honda RBPT"],
    "Williams": ["Williams", "Williams Ford", "Williams Honda", "Williams Renault", "Williams BMW", "Williams Cosworth", "Williams Toyota", "Williams Mecachrome", "Williams Supertec", "Williams Mercedes"],
    "Alfa Romeo": ["Alfa Romeo", "Sauber", "Sauber Mercedes", "Sauber Petronas", "Sauber BMW", "Alfa Romeo Racing Ferrari", "Kick Sauber Ferrari"],
    "Mercedes": ["Mercedes", "Brawn Mercedes"],
    "Aston Martin": ["Aston Martin Mercedes", "Aston Martin Aramco Mercedes"],
    "AlphaTauri": ["AlphaTauri Honda", "AlphaTauri RBPT", "AlphaTauri Honda RBPT"],
    "Benetton": ["Benetton BMW", "Benetton Ford", "Benetton Renault", "Benetton Playlife"],
    "Force India": ["Force India Ferrari", "Force India Mercedes", "Force India Sahara"],
    "Lotus": ["Lotus Climax", "Lotus BRM", "Lotus Ford", "Lotus Honda", "Lotus Judd", "Lotus Lamborghini", "Lotus Cosworth", "Lotus Mercedes"],
    "Minardi": ["Minardi Ford", "Minardi Ferrari", "Minardi Lamborghini", "Minardi Asiatech", "Minardi Cosworth"],
    "Toyota": ["Toyota", "Jordan Toyota", "MF1 Toyota"],
    "Jaguar": ["Jaguar Cosworth"],
    "Prost": ["Prost Mugen Honda", "Prost Peugeot", "Prost Acer"],
    "Haas": ["Haas Ferrari"],
    "Caterham": ["Caterham Renault"],
    "Virgin": ["Virgin Cosworth", "Marussia Cosworth", "Marussia Ferrari"],
    "HRT": ["HRT Cosworth"],
    "Spyker": ["Spyker Ferrari"],
    "Alpine": ["Alpine Renault"],
    "Toro Rosso": ["Toro Rosso", "Toro Rosso Ferrari", "Scuderia Toro Rosso Honda"],
    "Super Aguri": ["Super Aguri Honda"],
    "Racing Point": ["Racing Point BWT Mercedes"],
    "RB": ["RB Honda RBPT"],
}


def normalizar_equipo(nombre):
    if pd.isna(nombre):
        return None
    
    nombre = nombre.strip().lower()  # Convertimos a minúsculas y eliminamos espacios extra

    for nombre_normalizado, variantes in equipos_normalizados.items():
        if nombre in [v.lower() for v in variantes]:  # Comparación exacta
            return nombre_normalizado

    return nombre.title()  # Si no hay coincidencia exacta, devuelve el formato título
# Aplicamos la función a los DataFrames
teams_corrected['Team'] = teams['Team'].map(normalizar_equipo)
drivers_corrected['Car'] = drivers['Car'].map(normalizar_equipo)

def clean_driver_names(df, column_name="Driver"):
    df_cleaned = df.copy()  # Crear una copia del DataFrame original
    df_cleaned[column_name] = df_cleaned[column_name].astype(str).apply(lambda name: " ".join(name.split()))  # Limpiar espacios extra
    return df_cleaned

# Uso de la función
drivers_clean = clean_driver_names(drivers_corrected, column_name="Driver")


def clean_driver_names(df, column_name="Driver"):


    # Diccionario de correcciones manuales (errores comunes)
    name_corrections = {
        "Kimi RÃ¤ikkÃ¶nen": "Kimi Räikkönen",
        "Sergio Perez": "Sergio Pérez",
        "Nico Hulkenberg": "Nico Hülkenberg",
        "Zhou Guanyu": "Guanyu Zhou",
        "Jean Eric Vergne": "Jean-Éric Vergne",
        "Jerome d'Ambrosio": "Jérôme d'Ambrosio",
        "Carlos Sainz Jr.": "Carlos Sainz"
    }

    def normalize_name(name):
        # Elimina espacios extra dentro del nombre
        name = " ".join(name.split())
        
        # Normaliza caracteres (acentos y caracteres especiales)
        name = unicodedata.normalize("NFC", name)
        
        # Aplica correcciones específicas si el nombre está en el diccionario
        return name_corrections.get(name, name)

    # Aplicar la limpieza a la columna de nombres
    df[column_name] = df[column_name].apply(normalize_name)
    
    return df

df_clean_names = clean_driver_names(drivers_clean, column_name= "Driver")

drivers_per_country = df_clean_names.groupby("Nationality")["Code"].nunique()

drivers_per_country.sort_values(inplace = True, ascending= False)

# Crear la figura
plt.figure(figsize=(12, 6))

# Graficar barras
plt.bar(drivers_per_country.index, drivers_per_country.values)

# Ajustes del gráfico
sns.color_palette("pastel")
plt.xticks(rotation=90)  # Rotar etiquetas del eje X
plt.xlabel("Nationality")
plt.ylabel("Number of Drivers")
plt.title("Drivers per Country in F1")

st.pyplot(plt)

drivers_per_year = drivers.groupby("year")["Driver"].nunique()
plt.figure(figsize=(10,5))
sns.lineplot(x = drivers_per_year.index, y = drivers_per_year.values, marker = "o")
plt.xlabel("Year")
plt.ylabel("Drivers")
plt.title("Number of drivers per year")

st.pyplot(plt)

fastest_laps = fastest_laps.dropna(subset=["Time"])
fastest_laps["Time"] = "00:" + fastest_laps["Time"]  # Asegurar formato hh:mm:ss.sss
fastest_laps["Time"] = pd.to_timedelta(fastest_laps["Time"], errors="coerce")
fastest_laps["Time"] = fastest_laps["Time"].dt.total_seconds()

fastest_laps_per_year = fastest_laps.groupby('year')["Time"].mean()
plt.figure(figsize=(12,6))
sns.lineplot(x = fastest_laps_per_year.index, y= fastest_laps_per_year.values, marker = "o")
plt.xlabel("Year")
plt.ylabel(" AVG fastest lap (seconds)")

st.pyplot(plt)

teams_points_year = teams.groupby('Team')["PTS"].sum()
teams_points_year = teams_points_year[teams_points_year > 150]
teams_points_year = teams_points_year.sort_values(ascending=False)


plt.figure(figsize= (24, 6))
plt.bar(x = teams_points_year.index, height = teams_points_year.values)
plt.xticks(rotation=90)
plt.suptitle("Points won by team since 1958")
plt.title("* over 150")
plt.xlabel("Team")
plt.ylabel("Points")

st.pyplot(plt)

drivers_points = drivers.groupby("Driver")["PTS"].sum()
drivers_points = drivers_points.sort_values(ascending = False).head(10)


plt.figure(figsize= (12, 6))
plt.bar(x = drivers_points.index, height = drivers_points.values)
plt.xticks(rotation=90)
plt.title("Top 10 drivers by points")
plt.xlabel("Driver")
plt.ylabel("Points")

st.pyplot(plt)

