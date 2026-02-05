import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path

def normalize_number(value):
    if not value or value.strip() == '': return 0
    value = value.strip()
    if ':' in value:
        parts = value.split(':')
        if len(parts) == 3: return float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
        if len(parts) == 2: return float(parts[0])/60 + float(parts[1])/3600
    value = value.replace('%', '').replace(',', '.')
    parts = value.split('.')
    if len(parts) > 2: value = ''.join(parts[:-1]) + '.' + parts[-1]
    try: return float(value)
    except: return 0

def extract_id(text):
    if not text: return None
    text = text.strip()
    patterns = [r'(?:v=|/)([a-zA-Z0-9_-]{11})', r'^([a-zA-Z0-9_-]{11})$']
    for p in patterns:
        m = re.search(p, text)
        if m: return m.group(1)
    return None

def read_csv(path):
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            normalized = {}
            for k, v in row.items():
                if k: k = k.strip()
                if v: v = v.strip()
                if k in ['Fecha', 'Título del video', 'Contenido', 'Ubicación geográfica', 'Fuente de tráfico', 'Edad del usuario', 'Género del usuario', 'Tiempo de publicación del video']:
                    normalized[k] = v
                else:
                    normalized[k] = normalize_number(v)
            data.append(normalized)
        return data

def process_period(period_name, month_name_eng, year_str, content_p, geo_p, traffic_p, totals_p, age_p, gender_p):
    content = read_csv(content_p)
    geo = read_csv(geo_p)
    traffic = read_csv(traffic_p)
    totals = read_csv(totals_p)
    age = read_csv(age_p)
    gender = read_csv(gender_p)
    
    new_videos_count = 0
    new_shorts_count = 0
    new_standard_count = 0

    # Add thumbnails and count activity
    for row in content:
        if row.get('Contenido') and row['Contenido'] != 'Total':
            vid_id = extract_id(row['Contenido'])
            if vid_id:
                row['video_id'] = vid_id
                row['thumbnail_url'] = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"
                row['URL del vídeo'] = f"https://www.youtube.com/watch?v={vid_id}"
            
            # Count if published this month
            pub_date = row.get('Tiempo de publicación del video', '')
            if month_name_eng in pub_date and year_str in pub_date:
                new_videos_count += 1
                duration = row.get('Duración', 0)
                if duration > 0 and duration <= 60:
                    new_shorts_count += 1
                else:
                    new_standard_count += 1

    # Calculate KPIs from Total row of traffic or content
    kpis = {}
    total_row = next((r for r in traffic if r.get('Fuente de tráfico') == 'Total'), {})
    if not total_row: total_row = next((r for r in content if r.get('Contenido') == 'Total'), {})
    
    kpis['views'] = total_row.get('Vistas', 0)
    kpis['watch_time_hours'] = total_row.get('Tiempo de reproducción (horas)', 0)
    kpis['ctr'] = total_row.get('Tasa de clics de las impresiones (%)', 0)
    
    content_total = next((r for r in content if r.get('Contenido') == 'Total'), {})
    kpis['subscribers_gained'] = content_total.get('Suscriptores obtenidos', 0)
    kpis['subscribers_lost'] = content_total.get('Suscriptores perdidos', 0)
    kpis['likes'] = content_total.get('Me gusta', 0)
    kpis['impressions'] = content_total.get('Impresiones', 0)
    kpis['avg_watch_percentage'] = content_total.get('Porcentaje promedio reproducido (%)', 0)
    
    # Activity stats
    kpis['activity'] = {
        'total_published': new_videos_count,
        'shorts': new_shorts_count,
        'standard': new_standard_count
    }

    return {
        "metadata": {"period": period_name},
        "kpis": kpis,
        "content": {"table": [r for r in content if r.get('video_id')]},
        "geographic": {"table": [r for r in geo if r.get('Ubicación geográfica') and r.get('Ubicación geográfica') != 'Total']},
        "traffic": {"table": [r for r in traffic if r.get('Fuente de tráfico') and r.get('Fuente de tráfico') != 'Total'], "totals": totals},
        "demographics": {"age": age, "gender": gender}
    }

# Process Jan 2026
jan_data = process_period("2026-01", "Jan", "2026", "jan_content.csv", "jan_geo.csv", "jan_traffic.csv", "jan_totals.csv", "jan_age.csv", "jan_gender.csv")
print(f"Jan 2026: Kept {len(jan_data['content']['table'])} videos.")
for v in jan_data['content']['table'][:3]: print(f"  - {v['Título del video']} ({v['Vistas']} views)")

with open('youtube_analytics_jan_26.json', 'w', encoding='utf-8') as f:
    json.dump(jan_data, f, ensure_ascii=False, indent=2)

# Process Dec 2025
dec_data = process_period("2025-12", "Dec", "2025", "dec_content.csv", "dec_geo.csv", "dec_traffic.csv", "dec_totals.csv", "jan_age.csv", "jan_gender.csv")
with open('youtube_analytics_dec_25.json', 'w', encoding='utf-8') as f:
    json.dump(dec_data, f, ensure_ascii=False, indent=2)

print("Consolidated JSONs updated with activity counts.")
