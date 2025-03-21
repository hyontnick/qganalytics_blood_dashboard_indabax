from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Charger modèle, scaler et encodeurs au démarrage
model = joblib.load('/home/hyont-nick/INDABAX/BLOOD/APP/model/eligibility_model_rf_optimized.pkl')
scaler = joblib.load('/home/hyont-nick/INDABAX/BLOOD/APP/model/scaler_optimized.pkl')
le_dict = joblib.load('/home/hyont-nick/INDABAX/BLOOD/APP/model/label_encoders.pkl')

# Liste des features dans l'ordre exact attendu par le modèle
FEATURES = [
    'age', 'niveau_detude', 'genre', 'taille', 'poids', 'situation_matrimoniale_sm',
    'profession', 'arrondissement_de_residence', 'nationalite', 'religion',
    'a_til_elle_deja_donne_le_sang', 'taux_dhemoglobine', 'imc', 'jours_depuis_dernier_don'
]

# Fonction pour calculer l'IMC
def calculate_imc(taille, poids):
    return poids / ((taille/100) ** 2) if taille > 0 else -1

# Modèle Pydantic pour valider les entrées
class PredictionInput(BaseModel):
    age: int
    niveau_detude: str
    genre: str
    taille: float
    poids: float
    situation_matrimoniale_sm: str
    profession: str
    arrondissement_de_residence: str
    nationalite: str
    religion: str
    a_til_elle_deja_donne_le_sang: str
    si_oui_preciser_la_date_du_dernier_don: str  # Format YYYY-MM-DD ou vide
    taux_dhemoglobine: float

# Fonction pour encoder les données
def encode_input(data: dict):
    encoded = {}
    for feature in FEATURES:
        if feature == 'age':
            encoded[feature] = data['age']
        elif feature == 'taille':
            encoded[feature] = data['taille']
        elif feature == 'poids':
            encoded[feature] = data['poids']
        elif feature == 'taux_dhemoglobine':
            encoded[feature] = data['taux_dhemoglobine']
        elif feature == 'imc':
            encoded[feature] = calculate_imc(data['taille'], data['poids'])
        elif feature == 'jours_depuis_dernier_don':
            ref_date = pd.Timestamp('2025-03-18')
            date_input = data['si_oui_preciser_la_date_du_dernier_don']
            if date_input.strip() and data['a_til_elle_deja_donne_le_sang'].lower() == 'oui':
                date = pd.to_datetime(date_input, errors='coerce')
                encoded[feature] = (date - ref_date).days if not pd.isna(date) else -1
            else:
                encoded[feature] = -1
        else:
            try:
                encoded[feature] = le_dict[feature].transform([str(data[feature])])[0]
            except (KeyError, ValueError):
                encoded[feature] = -1
    return encoded

@app.post("/predict")
async def predict_eligibility(input_data: PredictionInput):
    try:
        # Convertir en dictionnaire
        data = input_data.dict()
        
        # Encoder les données
        encoded_data = encode_input(data)
        
        # Créer un DataFrame avec les features dans l’ordre exact
        input_df = pd.DataFrame([encoded_data], columns=FEATURES)
        
        # Remplacer les NaN par -1
        input_df.fillna(-1, inplace=True)
        
        # Standardiser les données
        input_scaled = scaler.transform(input_df)
        
        # Faire la prédiction avec les probabilités
        probability = model.predict_proba(input_scaled)[0]
        # Déterminer le résultat basé sur un seuil explicite de 0.5
        prediction = 1 if probability[1] >= 0.5 else 0
        result = "Éligible" if prediction == 1 else "Non éligible"
        
        return {
            "result": result,
            "probability_eligible": float(probability[1]),
            "probability_not_eligible": float(probability[0])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# lib a installer avant : pip install fastapi uvicorn requests '#1E88E5'
# Démarrer avec : uvicorn api:app --reload 
# ou avec cette commande (avec une IP et un Port specifique) : uvicorn api.api:app --reload --host 0.0.0.0 --port 8000