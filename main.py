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
    "users": [],
    "parcelas": []
}
contador_id_users = 1
contador_id_parcelas = 1

@app.post("/users")
async def registrar_o_login(request: Request):
    global contador_id_users
    user_data = await request.json()
    
    correo = user_data.get("email") or user_data.get("correo") or user_data.get("username")
    
    for u in db["users"]:
        if u.get("email") == correo or u.get("correo") == correo:
            return {"token": f"token_login_user_{u['id']}", "user": u}
            
    user_data["id"] = contador_id_users
    contador_id_users += 1
    db["users"].append(user_data)
    
    return {"token": f"token_nuevo_user_{user_data['id']}", "user": user_data}

@app.get("/parcelas")
async def get_parcelas():
    return db["parcelas"]

@app.post("/parcelas")
async def create_parcela(request: Request):
    global contador_id_parcelas
    parcela = await request.json()
    parcela["id"] = contador_id_parcelas
    contador_id_parcelas += 1
    db["parcelas"].append(parcela)
    return parcela

@app.put("/parcelas/{id}")
async def update_parcela(id: int, request: Request):
    datos = await request.json()
    for index, p in enumerate(db["parcelas"]):
        if p.get("id") == id:
            datos["id"] = id
            db["parcelas"][index] = datos
            return datos
    return {"error": "Parcela no encontrada"}

@app.delete("/parcelas/{id}")
async def delete_parcela(id: int):
    for index, p in enumerate(db["parcelas"]):
        if p.get("id") == id:
            db["parcelas"].pop(index)
            return {"mensaje": "Parcela eliminada exitosamente"}
    return {"error": "Parcela no encontrada"}
