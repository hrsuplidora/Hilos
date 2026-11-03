"""Prepara la carga de una exportación de HILOS (formato hilos-export-v1) en la base de una página nueva.

Uso:  python3 -I fase0/migracion/preparar_importacion.py <export.json> <carpeta de salida>

Escribe un archivo JSON por documento (<salida>/docs/<colección>/<id>.json) y lotes de escritura
(<salida>/lotes/lote-NN.json). Cada lote es la lista "writes" lista para pasar a ArtifactData action "batch":
50 entradas como máximo y menos de 900 KB de datos, con file_path absoluto para que el contenido no pase por la conversación.
"""
import json, os, sys

MAX_ENTRADAS = 50
MAX_BYTES = 900_000

def main(origen, salida):
    exp = json.load(open(origen, encoding="utf-8"))
    if exp.get("formato") != "hilos-export-v1":
        sys.exit("El archivo no es una exportación de HILOS (formato hilos-export-v1).")
    salida = os.path.abspath(salida)
    lotes, actual, tam = [], [], 0
    for col, docs in sorted(exp["colecciones"].items()):
        os.makedirs(os.path.join(salida, "docs", col), exist_ok=True)
        for doc_id, data in sorted(docs.items()):
            ruta = os.path.join(salida, "docs", col, doc_id + ".json")
            texto = json.dumps(data, ensure_ascii=False)
            open(ruta, "w", encoding="utf-8").write(texto)
            n = len(texto.encode("utf-8"))
            if actual and (len(actual) >= MAX_ENTRADAS or tam + n > MAX_BYTES):
                lotes.append(actual); actual, tam = [], 0
            actual.append({"op": "set", "collection": col, "doc_id": doc_id, "file_path": ruta})
            tam += n
    if actual:
        lotes.append(actual)
    os.makedirs(os.path.join(salida, "lotes"), exist_ok=True)
    for i, lote in enumerate(lotes, 1):
        json.dump(lote, open(os.path.join(salida, "lotes", f"lote-{i:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"manifiesto": exp["manifiesto"], "total": exp["total"], "lotes": len(lotes),
                      "carpeta_lotes": os.path.join(salida, "lotes")}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
