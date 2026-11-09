from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Cultivos")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = {
    "parcelas": []
}
contador_id = 1

@app.post("/users")
async def login(request: Request):
    user_data = await request.json()
    return {"token": "token_python_super_seguro_123"}

@app.get("/parcelas")
async def get_parcelas():
    return db["parcelas"]

@app.post("/parcelas")
async def create_parcela(request: Request):
    global contador_id
    parcela = await request.json()
    
    parcela["id"] = contador_id
    contador_id += 1
    
    db["parcelas"].append(parcela)
    return parcela

@app.put("/parcelas/{id}")
async def update_parcela(id: int, request: Request):
    datos_actualizados = await request.json()
    for index, p in enumerate(db["parcelas"]):
        if p.get("id") == id:
            datos_actualizados["id"] = id
            db["parcelas"][index] = datos_actualizados
            return datos_actualizados
    return {"error": "Parcela no encontrada"}

@app.delete("/parcelas/{id}")
async def delete_parcela(id: int):
    for index, p in enumerate(db["parcelas"]):
        if p.get("id") == id:
            db["parcelas"].pop(index)
            return {"mensaje": "Parcela eliminada exitosamente"}
    return {"error": "Parcela no encontrada"}