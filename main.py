from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_database_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
############ rodrigo.rejala@outlook.com ##############

@app.get("/ruc/")
async def ruc (numero_ruc : int = Query(..., description="Numero de RUC a buscar")):
    if not validar_ruc(numero_ruc):
        raise HTTPException(
            status_code=400,
            detail="Formato de Ruc invalido, debe ser un numero"
        )
    conn = get_database_connection()
    cursor = conn.cursor()
    try: 
        query = "SELECT nombre_completo, ruc, dv, estado FROM rucpy WHERE ruc = ? LIMIT 1"
        result = cursor.execute(query, (numero_ruc,)).fetchone()
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Ruc no encontrado"
            )
        return {
            "nombre_razonsocial" : result[0],
            "ruc" : result[1],
            "digito_verificador" : result[2],
            "estado" : result[3]
        }
    finally:
        conn.close()

##################################################################################################

@app.get("/nombre_razonsocial/")
async def nombre_razonsocial(nombre_completo: str = Query(..., min_length=3, description="Nombre o parte del nombre a buscar")):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        # Dividir el nombre en palabras individuales
        palabras = nombre_completo.lower().split()
        
        # Construir condiciones LIKE para cada palabra
        condiciones = " AND ".join(["LOWER(nombre_completo) LIKE ?" for _ in palabras])
        parametros = [f"%{palabra}%" for palabra in palabras]

        query = f"""
        SELECT nombre_completo, ruc, dv, estado
        FROM rucpy
        WHERE {condiciones}
        ORDER BY nombre_completo
        LIMIT 100
        """
        
        cursor.execute(query, parametros)
        result = cursor.fetchall()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron coincidencias. Pruebe con un término más general o menos palabras."
            )

        return [
            {
                "nombre_razonsocial": fila[0],
                "ruc": fila[1],
                "dv": fila[2],
                "estado": fila[3]
            } for fila in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")
    finally:
        conn.close()

################################################################################################

@app.get("/")
def read_root():
    return {"Hello":"Esto es un BACKEND desarrollado por rodrigo.rejala@outlook.com"}


#$!@$@!%$!!!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#!@#

def validar_ruc(numero_ruc : int) -> bool:
    ruc_str = str(numero_ruc)
    return len(ruc_str) >= 7
