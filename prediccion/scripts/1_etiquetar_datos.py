"""
PASO 1: Etiquetar datos usando heurísticas
Genera dataset etiquetado a partir de profiles y posts existentes
"""
import os
import sys
import json
import yaml
import pandas as pd
from pathlib import Path

# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from prediccion.utils.feature_extraction import FeatureExtractor
from prediccion.utils.heuristics import HeuristicLabeler

def cargar_config():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def cargar_datos(config):
    """Carga profiles y posts desde los archivos JSON"""
    base_dir = Path(__file__).parent.parent
    
    # Cargar profiles
    profiles_path = base_dir / config['rutas']['profiles_input']
    print(f"📖 Cargando profiles desde: {profiles_path}")
    with open(profiles_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    print (f"✓ {len(profiles)} perfiles cargados")
    
    # Cargar posts
    posts_path = base_dir / config['rutas']['posts_input']
    print(f"📖 Cargando posts desde: {posts_path}")
    with open(posts_path, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    print(f"✓ {len(posts_data)} usuarios con posts cargados")
    
    return profiles, posts_data

def etiquetar_perfiles(profiles, posts_data, config):
    """
    Etiqueta perfiles usando heurísticas
    
    Returns:
        DataFrame con features y labels
    """
    print("\n🏷️  Iniciando etiquetado heurístico...")
    
    extractor = FeatureExtractor()
    labeler = HeuristicLabeler(config['heuristicas'])
    
    data = []
    etiquetados = {'bots': 0, 'humanos': 0, 'inciertos': 0}
    
    for i, profile in enumerate(profiles):
        if (i + 1) % 1000 == 0:
            print(f"  Procesados: {i+1}/{len(profiles)}")
        
        did = profile.get('did')
        if not did:
            continue
        
        # Obtener posts del usuario (si existen)
        user_posts = None
        if did in posts_data:
            user_posts = posts_data[did].get('posts', [])
        
        # Extraer features
        try:
            features = extractor.extract_profile_features(profile, user_posts)
        except Exception as e:
            print(f"  ⚠️ Error extrayendo features de {did}: {e}")
            continue
        
        # Etiquetar con heurísticas
        label = labeler.label_profile(features)
        
        # Contar
        if label == 1:
            etiquetados['bots'] += 1
        elif label == 0:
            etiquetados['humanos'] += 1
        else:
            etiquetados['inciertos'] += 1
        
        # Guardar datos (incluso inciertos, los filtraremos después)
        row = features.copy()
        row['did'] = did
        row['handle'] = profile.get('handle', '')
        row['label'] = label
        data.append(row)
    
    print(f"\n📊 Etiquetado completado:")
    print(f"  • Bots: {etiquetados['bots']}")
    print(f"  • Humanos: {etiquetados['humanos']}")
    print(f"  • Inciertos: {etiquetados['inciertos']}")
    
    # Verificar que hay datos
    if not data:
        print("\n❌ ERROR: No se pudieron extraer features de ningún perfil")
        print("   Verifica que los archivos JSON tengan el formato correcto")
        return pd.DataFrame()  # DataFrame vacío
    
    df = pd.DataFrame(data)
    
    # Filtrar inciertos (label == -1)
    df_etiquetado = df[df['label'] != -1].copy()
    print(f"\n✓ Dataset final: {len(df_etiquetado)} perfiles etiquetados")
    print(f"  (Descartados {len(df) - len(df_etiquetado)} inciertos)")
    
    return df_etiquetado

def guardar_dataset(df, config):
    """Guarda el dataset etiquetado"""
    base_dir = Path(__file__).parent.parent
    output_path = base_dir / config['rutas']['dataset_etiquetado']
    
    # Crear directorio si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\n💾 Dataset guardado en: {output_path}")
    print(f"📊 Tamaño: {len(df)} filas x {len(df.columns)} columnas")
    
    # Mostrar distribución de labels
    print(f"\n📈 Distribución de labels:")
    print(df['label'].value_counts())
    
    return output_path

def main():
    print("=" * 80)
    print("PASO 1: ETIQUETADO DE DATOS CON HEURÍSTICAS")
    print("=" * 80)
    
    # Cargar configuración
    config = cargar_config()
    
    # Cargar datos
    profiles, posts_data = cargar_datos(config)
    
    # Etiquetar perfiles
    df_etiquetado = etiquetar_perfiles(profiles, posts_data, config)
    
    # Guardar dataset
    output_path = guardar_dataset(df_etiquetado, config)
    
    print("\n" + "=" * 80)
    print("✅ ETIQUETADO COMPLETADO")
    print("=" * 80)
    print(f"\n📁 Dataset etiquetado: {output_path}")
    print("➡️  Siguiente paso: python scripts/2_entrenar_modelo.py")

if __name__ == "__main__":
    main()
