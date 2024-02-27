import pandas as pd

# Charger le fichier Excel dans un dataframe
df_original = pd.read_excel("Meetings of Commission representatives of the Von der leyen Commission (2019-2024).xlsx", skiprows=1)

# Créer le dataframe df_final avec les colonnes requises
df_final = pd.DataFrame(columns=["Interest_ID", "Name_Of_Cabinet", "Subject", "Date_Of_Meeting", "Location", "EC_Representative_Involved"])

# Parcourir chaque ligne du dataframe original
for index, row in df_original.iterrows():
    # Scinder les valeurs de la colonne "Transparency register ID" par virgule
    transparency_ids = row["Transparency register ID"].split(",")
    
    # Pour chaque transparence ID, créer une nouvelle ligne dans df_final avec les autres colonnes dupliquées
    for transparency_id in transparency_ids:
        new_row = {
            "Interest_ID": transparency_id.strip(),
            "Name_Of_Cabinet": row["Name of cabinet"],
            "Subject": row["Subject of the meeting"],
            "Date_Of_Meeting": row["Date of meeting"],
            "Location": row["Location"],
            "EC_Representative_Involved": row["Name of EC representative"]
        }
        df_final = df_final._append(new_row, ignore_index=True)



# Exporter df_final au format CSV avec un point-virgule comme séparateur
df_final.to_csv("commission_meetings.csv", sep=";", encoding="utf-8", index=False)