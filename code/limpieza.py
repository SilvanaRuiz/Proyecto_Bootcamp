import re
import pandas as pd 

def con_a_meses(hosting_time):
    # Buscar "years" y convertir a meses
    years_match = re.search(r'(\d+)\s+years?', hosting_time)
    if years_match:
        years = int(years_match.group(1))
        return years * 12
    
    # Buscar "months" y dejar en meses
    months_match = re.search(r'(\d+)\s+months?', hosting_time)
    if months_match:
        months = int(months_match.group(1))
        return months
    
    # Buscar "days" y convertir a meses (aprox. 30 días = 1 mes)
    days_match = re.search(r'(\d+)\s+days?', hosting_time)
    if days_match:
        days = int(days_match.group(1))
        return days / 30  # Convertir días a meses
    
    return 0  # Si no hay coincidencia, devolver 0 meses

def extract_price(price):
    if isinstance(price, str):  # Asegurarse de que la entrada sea un string
        match = re.search(r'[€$]\s*(\d+)', price)
        if match:
            return float(match.group(1))  # Convertir a float
    return None  # Si no hay coincidencia o no es string, devuelve None

def extract_guest(guest):
    if isinstance(guest, str):
        match = re.search(r'(\d+)\s+guests', guest)
        if match:
            return float(match.group(1))
    return None

def extract_bedroom(room):
    if isinstance(room, str):
        match = re.search(r'(\d+)\s+bedroom(s)?', room)
        if match:
            return float(match.group(1))
        if re.search(r'\bstudio\b', room, re.IGNORECASE):
            return 1
    return None

def extract_bed(bed):
    if isinstance(bed, str):
        match = re.search(r'(\d+)\s+(?:\w+\s+)?(?:bed|beds)(?!room)', bed, re.IGNORECASE)
        if match:
            return float(match.group(1))  
    return None

def extract_bathroom(bath):
    if isinstance(bath, float) and pd.isna(bath):
        return "unknown"  # Retorna un valor por defecto si es NaN
    elif isinstance(bath, str):
        if re.search(r'\bshared\b', bath, re.IGNORECASE):
            return "shared"
        else:
            return "private"
    else:
        return "unknown"

def extract_number_of_baths(bath):
    if isinstance(bath, float) and pd.isna(bath):
        return 1  # Valor por defecto para NaN
    elif isinstance(bath, str):
        if re.search(r'\bshared\b', bath, re.IGNORECASE):
            return 1  # Si es shared, retorna 1 por defecto
        match = re.search(r'(\d+)\s*\w*\s*baths?', bath, re.IGNORECASE)
        if match:
            return int(match.group(1))  # Retorna el número de baños
    return 1  # Valor por defecto si no se encuentra información

def limpiezadedatos(df):
    df['rating'] = df['rating'].str.extract(r'(\d\.\d{1,2})$').astype(float)
    df['number_reviews'] = pd.to_numeric(df['number_reviews'], errors='coerce')
    df['price'] = df['price'].apply(extract_price)
    df['hosting_time'] = df['hosting_time'].apply(con_a_meses)
    df['guest_favorite'] = df['guest_favorite'].astype(int)

    # Rellena NaN en `complete_data_list` con un valor predeterminado
    df['complete_data_list'] = df['complete_data_list'].fillna("unknown")

    # Aplica las funciones de extracción
    df['number_guest'] = df['complete_data_list'].apply(extract_guest)
    df['number_bedroom'] = df['complete_data_list'].apply(extract_bedroom)
    df['number_beds'] = df['complete_data_list'].apply(extract_bed)
    df['type_bathroom'] = df['complete_data_list'].apply(extract_bathroom)
    df['number_bathroom'] = df['complete_data_list'].apply(extract_number_of_baths)
    df.drop(columns='complete_data_list', inplace=True)
    
    return df
