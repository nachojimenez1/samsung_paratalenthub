import json

with open('lexi_database_FULL.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mapa_final = {}

for deporte, categorias in data.items():
    for cat, info in categorias.items():
        for perfil in info['perfiles_visuales']:
            img = perfil['archivo_local']
            if img not in mapa_final:
                mapa_final[img] = []
            
            entrada = f"{deporte} - {cat}"
            if entrada not in mapa_final[img]:
                mapa_final[img].append(entrada)

with open('mapa_deportes.json', 'w', encoding='utf-8') as f:
    json.dump(mapa_final, f, indent=4)

print("✅ Mapa de deportes creado. Ahora el sistema sabe qué deportes corresponden a cada imagen.")