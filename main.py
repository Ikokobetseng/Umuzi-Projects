import pandas as pd
import numpy as np
from datetime import datetime

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def clean_data(data):
    # Normalize column names
    data.columns = [col.lower().replace(' ', '_') for col in data.columns]

    # Clean full_name and nationality
    data['full_name'] = data['full_name'].str.strip().str.title()
    data['nationality'] = data['nationality'].str.strip().str.title()

    # Standardize gender
    gender_map = {
        'male': 'Male', 'm': 'Male', 'man': 'Male', 'boy': 'Male',
        'female': 'Female', 'f': 'Female', 'woman': 'Female', 'girl': 'Female'
    }
    data['gender'] = data['gender'].str.lower().map(gender_map).fillna('Other')

    # Clean income
    #data['income'] = data['income'].astype(str).str.replace('[^\d\.]', '', regex=True).astype(float)
    data['income'] = data['income'].astype(str).str.replace(r'[^\d\.]', '', regex=True).astype(float)

    # Fix birth_date and calculate age
    data['birth_date'] = pd.to_datetime(data['birth_date'], errors='coerce')
    data['age'] = data['birth_date'].apply(lambda x: (datetime.today() - x).days / 365 if not pd.isnull(x) else np.nan)

    # Standardize is_employed
    data['is_employed'] = data['is_employed'].astype(str).str.lower()
    data['is_employed'] = data['is_employed'].map({
        'yes': True, 'y': True, '1': True, 'true': True,
        'no': False, 'n': False, '0': False, 'false': False
    })

    # Drop duplicates and rows with missing values
    data['email'] = data['email'].str.lower()
    data = data.drop_duplicates(subset='email', keep='first')
    critical_columns = ['email', 'birth_date', 'income']
    data = data.dropna(subset=critical_columns)

    return data

def main():
    file_path = 'https://raw.githubusercontent.com/Umuzi-org/data-wrangling-Ikokobetseng/refs/heads/main/data/wrangling_data.csv?token=GHSAT0AAAAAADFO3O4IIAGAMPPIMPPHOKX42CQRKEA'
    data = load_data(file_path)
    if data is not None:
        cleaned_data = clean_data(data)
        print(cleaned_data)

if __name__ == "__main__":
    main()
