import pandas as pd
from pathlib import Path

# Cargar dataset (path absoluto)
script_dir = Path(__file__).parent.parent
df = pd.read_csv(script_dir / 'datos' / 'dataset_etiquetado.csv')

# Calcular estadísticas
total_original = 14900
total_etiquetado = len(df)
bots = (df['label'] == 1).sum()
humanos = (df['label'] == 0).sum()
inciertos = total_original - total_etiquetado

# Porcentajes
pct_etiquetado = (total_etiquetado / total_original) * 100
pct_inciertos = (inciertos / total_original) * 100
pct_bots_dataset = (bots / total_etiquetado) * 100
pct_humanos_dataset = (humanos / total_etiquetado) * 100

# Mostrar resultados
print("\n" + "="*60)
print("📊 RESULTADOS DEL ETIQUETADO FINAL")
print("="*60)
print(f"\n🔢 TOTALES:")
print(f"  Perfiles originales:     {total_original:,}")
print(f"  Perfiles etiquetados:    {total_etiquetado:,} ({pct_etiquetado:.1f}%)")
print(f"  Perfiles inciertos:      {inciertos:,} ({pct_inciertos:.1f}%)")

print(f"\n🏷️  DISTRIBUCIÓN DEL DATASET:")
print(f"  Bots:                    {bots:,} ({pct_bots_dataset:.1f}%)")
print(f"  Humanos:                 {humanos:,} ({pct_humanos_dataset:.1f}%)")

print(f"\n✅ VALIDACIÓN DE OBJETIVOS:")
print(f"  Objetivo inciertos < 5%: {'✅ CUMPLIDO' if pct_inciertos < 5 else f'❌ NO ({pct_inciertos:.1f}%)'}")
print(f"  Objetivo bots ~5%:       {'✅ CERCA' if 3 <= pct_bots_dataset <= 10 else f'❌ NO ({pct_bots_dataset:.1f}%)'}")

print("="*60 + "\n")
