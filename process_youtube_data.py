"""
YouTube Analytics Data Processor for IdeaPaís Dashboard

Este script procesa y normaliza múltiples CSVs de YouTube Analytics
para crear archivos JSON consolidados que el dashboard puede consumir fácilmente.

Estructura de entrada:
- Área geográfica/: Datos de la tabla.csv, Datos del gráfico.csv, Totales.csv
- Contenido/: Datos de la tabla.csv, Datos del gráfico.csv, Totales.csv  
- Fuente de tráfico/: Datos de la tabla.csv, Datos del gráfico.csv, Totales.csv

Salida:
- youtube_analytics_processed.json: Archivo consolidado con todos los datos normalizados
"""

import csv
import json
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class YouTubeDataProcessor:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.data = {
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'period': None
            },
            'geographic': {
                'table': [],
                'chart': [],
                'totals': []
            },
            'content': {
                'table': [],
                'chart': [],
                'totals': []
            },
            'traffic': {
                'table': [],
                'chart': [],
                'totals': []
            },
            'kpis': {}
        }
    
    def normalize_string(self, text: str) -> str:
        """Normaliza string removiendo acentos"""
        # Decompose characters and remove accents
        nfkd = unicodedata.normalize('NFKD', text)
        return ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    def find_folders(self) -> Dict[str, Path]:
        """Encuentra las 3 carpetas críticas de datos"""
        folders = {}
        
        for item in self.base_dir.iterdir():
            if not item.is_dir():
                continue
                
            name = item.name
            name_normalized = self.normalize_string(name.lower())
            
            if 'geografica' in name_normalized or 'area' in name_normalized:
                folders['geographic'] = item
                print(f"✓ Encontrada carpeta Geográfica: {name}")
                # Extract period from folder name
                if not self.data['metadata']['period']:
                    period_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2})', name)
                    if period_match:
                        self.data['metadata']['period'] = period_match.group(1)
                        
            elif 'contenido' in name_normalized:
                folders['content'] = item
                print(f"✓ Encontrada carpeta Contenido: {name}")
                
            elif 'trafico' in name_normalized or 'fuente' in name_normalized:
                folders['traffic'] = item
                print(f"✓ Encontrada carpeta Tráfico: {name}")
        
        return folders
    
    def normalize_number(self, value: str) -> Optional[float]:
        """Normaliza números en formato español a float"""
        if not value or value.strip() == '':
            return None
        
        # Remove whitespace
        value = value.strip()
        
        # Handle time format (HH:MM:SS or MM:SS)
        if ':' in value:
            try:
                parts = value.split(':')
                if len(parts) == 3:  # HH:MM:SS
                    hours = float(parts[0])
                    minutes = float(parts[1])
                    seconds = float(parts[2])
                    return hours + (minutes / 60) + (seconds / 3600)
                elif len(parts) == 2:  # MM:SS
                    minutes = float(parts[0])
                    seconds = float(parts[1])
                    return (minutes / 60) + (seconds / 3600)
            except ValueError:
                return None
        
        # Handle percentage (remove %)
        if '%' in value:
            value = value.replace('%', '')
        
        # Replace comma with dot for decimal
        value = value.replace(',', '.')
        
        # Remove thousands separators (dots in Spanish format)  
        # Be careful: 1.234,56 becomes 1234.56
        parts = value.split('.')
        if len(parts) > 2:  # Has thousands separator
            value = ''.join(parts[:-1]) + '.' + parts[-1]
        
        try:
            return float(value)
        except ValueError:
            return None
    
    def read_csv(self, filepath: Path) -> List[Dict[str, Any]]:
        """Lee y normaliza un archivo CSV"""
        if not filepath.exists():
            print(f"⚠️  Archivo no encontrado: {filepath}")
            return []
        
        data = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                print(f"📄 Leyendo {filepath.name}: {len(headers)} columnas")
                
                for row in reader:
                    # Skip empty rows
                    if not any(row.values()):
                        continue
                    
                    # Normalize numeric values
                    normalized_row = {}
                    for key, value in row.items():
                        if value and value.strip():
                            # Try to convert to number
                            num_value = self.normalize_number(value)
                            if num_value is not None and key != 'Fecha' and 'Contenido' not in key and 'Título' not in key and 'URL' not in key:
                                normalized_row[key] = num_value
                            else:
                                normalized_row[key] = value.strip()
                        else:
                            normalized_row[key] = None
                    
                    data.append(normalized_row)
                
                print(f"   ✓ {len(data)} filas procesadas")
                
        except Exception as e:
            print(f"❌ Error leyendo {filepath}: {e}")
        
        return data
    
    def process_folder(self, folder: Path, data_key: str):
        """Procesa los 3 CSVs de una carpeta"""
        print(f"\n📁 Procesando: {folder.name}")
        
        # Datos de la tabla
        table_file = folder / "Datos de la tabla.csv"
        self.data[data_key]['table'] = self.read_csv(table_file)
        
        # Datos del gráfico (time series)
        chart_file = folder / "Datos del gráfico.csv"
        self.data[data_key]['chart'] = self.read_csv(chart_file)
        
        # Totales
        totals_file = folder / "Totales.csv"
        self.data[data_key]['totals'] = self.read_csv(totals_file)
    
    def calculate_kpis(self):
        """Calcula KPIs principales desde los datos procesados"""
        print("\n📊 Calculando KPIs...")
        
        # Get traffic totals (first row is "Total")
        if self.data['traffic']['table']:
            traffic_total = self.data['traffic']['table'][0]  # First row is Total
            
            self.data['kpis']['views'] = traffic_total.get('Vistas', 0)
            self.data['kpis']['watch_time_hours'] = traffic_total.get('Tiempo de reproducción (horas)', 0)
            self.data['kpis']['ctr'] = traffic_total.get('Tasa de clics de las impresiones (%)', 0)
        
        # Get content totals
        if self.data['content']['table']:
            content_total = self.data['content']['table'][0]  # First row is Total
            
            self.data['kpis']['subscribers_gained'] = content_total.get('Suscriptores obtenidos', 0)
            self.data['kpis']['subscribers_lost'] = content_total.get('Suscriptores perdidos', 0)
            self.data['kpis']['avg_watch_percentage'] = content_total.get('Porcentaje promedio reproducido (%)', 0)
            self.data['kpis']['likes'] = content_total.get('Me gusta', 0)
            self.data['kpis']['comments'] = content_total.get('Comentarios agregados', 0)
        
        print(f"   ✓ KPIs calculados: {len(self.data['kpis'])} métricas")
    
    def extract_video_thumbnails(self):
        """Extrae IDs de video y genera URLs de thumbnails"""
        print("\n🎬 Procesando thumbnails de videos...")
        
        video_count = 0
        for video in self.data['content']['table'][1:]:  # Skip Total row
            # Look for URL field (might be "URL del vídeo" or similar)
            url = None
            for key in video.keys():
                if 'URL' in key or 'url' in key:
                    url = video.get(key)
                    break
            
            if url:
                # Extract video ID from YouTube URL
                video_id = self.extract_video_id(url)
                if video_id:
                    video['video_id'] = video_id
                    video['thumbnail_url'] = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                    video_count += 1
        
        print(f"   ✓ {video_count} videos con thumbnails")
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrae el ID de video de una URL de YouTube"""
        if not url:
            return None
        
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def process_all(self) -> Dict[str, Any]:
        """Proceso principal"""
        print("=" * 60)
        print("🚀 YouTube Analytics Data Processor - IdeaPaís")
        print("=" * 60)
        
        # Find folders
        folders = self.find_folders()
        
        if len(folders) != 3:
            print(f"\n⚠️  Se esperaban 3 carpetas, se encontraron {len(folders)}")
            print(f"   Carpetas encontradas: {list(folders.keys())}")
        
        # Process each folder
        if 'geographic' in folders:
            self.process_folder(folders['geographic'], 'geographic')
        
        if 'content' in folders:
            self.process_folder(folders['content'], 'content')
        
        if 'traffic' in folders:
            self.process_folder(folders['traffic'], 'traffic')
        
        # Calculate KPIs
        self.calculate_kpis()
        
        # Add video thumbnails
        self.extract_video_thumbnails()
        
        return self.data
    
    def save_json(self, output_file: str = 'youtube_analytics_processed.json'):
        """Guarda los datos procesados en JSON"""
        output_path = self.base_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        file_size = output_path.stat().st_size / 1024  # KB
        
        print("\n" + "=" * 60)
        print(f"✅ Datos procesados guardados en: {output_path.name}")
        print(f"   Tamaño: {file_size:.2f} KB")
        print("=" * 60)
        
        return output_path


def main():
    """Main entry point - Legacy wrapper"""
    pass
    print(f"   • Países/regiones: {len(processor.data['geographic']['table']) - 1}")
    print(f"   • KPIs calculados: {len(processor.data['kpis'])}")
    print("\nEjecución completada exitosamente! 🎉")


if __name__ == '__main__':
    main()
