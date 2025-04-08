# notifications.py
import sqlite3
from datetime import datetime

# Chemin de la base de données SQLite
DB_PATH = "blood_donation_users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            email TEXT,
            numero_telephone TEXT,
            age INTEGER,
            niveau_detude TEXT,
            genre TEXT,
            taille REAL,
            poids REAL,
            situation_matrimoniale_sm TEXT,
            profession TEXT,
            arrondissement_de_residence TEXT,
            nationalite TEXT,
            religion TEXT,
            a_til_elle_deja_donne_le_sang TEXT,
            si_oui_preciser_la_date_du_dernier_don TEXT,
            taux_dhemoglobine REAL,
            result TEXT,
            probability_eligible REAL,
            probability_not_eligible REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Sauvegarder toutes les données dans la BD
def save_user_data(user_info):
    # S'assurer que la table existe avant d'insérer
    init_db()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (
            nom, email, numero_telephone, age, niveau_detude, genre, taille, poids,
            situation_matrimoniale_sm, profession, arrondissement_de_residence,
            nationalite, religion, a_til_elle_deja_donne_le_sang,
            si_oui_preciser_la_date_du_dernier_don, taux_dhemoglobine,
            result, probability_eligible, probability_not_eligible, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_info["nom"],
        user_info["email"],
        user_info["numero_telephone"],
        user_info["data"]["age"],
        user_info["data"]["niveau_detude"],
        user_info["data"]["genre"],
        user_info["data"]["taille"],
        user_info["data"]["poids"],
        user_info["data"]["situation_matrimoniale_sm"],
        user_info["data"]["profession"],
        user_info["data"]["arrondissement_de_residence"],
        user_info["data"]["nationalite"],
        user_info["data"]["religion"],
        user_info["data"]["a_til_elle_deja_donne_le_sang"],
        user_info["data"]["si_oui_preciser_la_date_du_dernier_don"],
        user_info["data"]["taux_dhemoglobine"],
        user_info["result"],
        user_info["probability_eligible"],
        user_info["probability_not_eligible"],
        user_info["timestamp"]
    ))
    conn.commit()
    conn.close()

# Plus besoin d'appeler init_db() ici, car il est appelé dans save_user_data