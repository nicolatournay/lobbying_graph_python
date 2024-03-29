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

# Charger le fichier interest.xls dans un dataframe df_interest
df_interest = pd.read_excel("interest.xls")

# Ajouter les nouvelles colonnes à df_final en effectuant une jointure interne avec df_interest
df_final = df_final.merge(df_interest[["Identification code", "Name", "Acronym", "Category of registration", "Website URL", "Closed year EU grant: amount (source)", "Current year EU grant: source (amount)"]],
                            left_on="Interest_ID",
                            right_on="Identification code",
                            how="left")

# Renommer les colonnes ajoutées
df_final = df_final.rename(columns={"Name": "Interest_Name",
                                    "Acronym": "Interest_Acronym",
                                    "Category of registration": "Interest_Category",
                                    "Website URL": "Interest_URL",
                                    "Closed year EU grant: amount (source)": "Closed_year_EU_grant",
                                    "Current year EU grant: source (amount)": "Current_year_EU_grant"})

# Supprimer la colonne "Identification code" qui n'est plus nécessaire
df_final = df_final.drop(columns="Identification code")

for index, row in df_final.iterrows():
    # Vérifier si la colonne "Name" est vide
    if pd.isna(row["Interest_Name"]):
        # Essayer de trouver les informations dans les fichiers annuels
        found = False
        for year in range(2023, 2018, -1):  # De 2023 à 2019
            try:
                df_yearly = pd.read_excel(f"interest_{year}.xls")
                match_row = df_yearly[df_yearly["Identification code"] == row["Interest_ID"]].iloc[0]
                df_final.at[index, ["Interest_Name", "Interest_Acronym", "Interest_Category", "Interest_URL", "Closed_year_EU_grant", "Current_year_EU_grant"]] = match_row[["Name", "Acronym", "Category of registration", "Website URL", "Closed year EU grant: amount (source)", "Current year EU grant: source (amount)"]]
                found = True
                break
            except (FileNotFoundError, IndexError):
                # Fichier non trouvé ou aucune correspondance, passer à l'année suivante
                continue
        
        if not found:
            print(f"No match found for Interest_ID {row['Interest_ID']} in any year from 2019 to 2023.")


# Exporter df_final au format CSV avec un point-virgule comme séparateur
df_final.to_csv("edges.csv", sep=";", encoding="utf-8", index=False)