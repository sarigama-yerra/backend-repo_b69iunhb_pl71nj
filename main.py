import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import create_document, get_documents
from schemas import Account, Plan, Angebot, Beratung, ServiceTicket, Inspiration

app = FastAPI(title="LIVARO Home API", description="Backend für LIVARO Home – Account, Planer, Dashboard, Beratung, Angebote, Service, Inspiration", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "LIVARO Home API", "status": "ok"}

@app.get("/test")
def test_database():
    from database import db
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set" if not os.getenv("DATABASE_URL") else "✅ Set",
        "database_name": "❌ Not Set" if not os.getenv("DATABASE_NAME") else "✅ Set",
        "collections": []
    }
    try:
        if db is None:
            status["database"] = "❌ Not Connected"
        else:
            status["database"] = "✅ Connected"
            try:
                status["collections"] = db.list_collection_names()[:20]
            except Exception as e:
                status["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
    except Exception as e:
        status["database"] = f"❌ Error: {str(e)[:80]}"
    return status

# Helper to map class name to collection name

def collection_name(model_cls) -> str:
    return model_cls.__name__.lower()

# Generic create endpoints for core modules

@app.post("/account", response_model=dict)
def create_account(payload: Account):
    try:
        _id = create_document(collection_name(Account), payload)
        return {"id": _id, "message": "Account angelegt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/account", response_model=List[dict])
def list_accounts(email: Optional[EmailStr] = None, limit: int = 50):
    try:
        f = {"email": str(email)} if email else {}
        return get_documents(collection_name(Account), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/plan", response_model=dict)
def create_plan(payload: Plan):
    try:
        _id = create_document(collection_name(Plan), payload)
        return {"id": _id, "message": "Plan erstellt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/plan", response_model=List[dict])
def list_plans(account_email: Optional[EmailStr] = None, limit: int = 50):
    try:
        f = {"account_email": str(account_email)} if account_email else {}
        return get_documents(collection_name(Plan), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/angebot", response_model=dict)
def create_angebot(payload: Angebot):
    try:
        _id = create_document(collection_name(Angebot), payload)
        return {"id": _id, "message": "Angebot erstellt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/angebot", response_model=List[dict])
def list_angebote(plan_id: Optional[str] = None, status: Optional[str] = None, limit: int = 50):
    try:
        f = {}
        if plan_id:
            f["plan_id"] = plan_id
        if status:
            f["status"] = status
        return get_documents(collection_name(Angebot), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/beratung", response_model=dict)
def create_beratung(payload: Beratung):
    try:
        _id = create_document(collection_name(Beratung), payload)
        return {"id": _id, "message": "Beratungsanfrage erfasst"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/beratung", response_model=List[dict])
def list_beratungen(account_email: Optional[EmailStr] = None, limit: int = 50):
    try:
        f = {"account_email": str(account_email)} if account_email else {}
        return get_documents(collection_name(Beratung), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/service", response_model=dict)
def create_service(payload: ServiceTicket):
    try:
        _id = create_document(collection_name(ServiceTicket), payload)
        return {"id": _id, "message": "Service-Ticket erstellt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/service", response_model=List[dict])
def list_service(account_email: Optional[EmailStr] = None, status: Optional[str] = None, limit: int = 50):
    try:
        f = {}
        if account_email:
            f["account_email"] = str(account_email)
        if status:
            f["status"] = status
        return get_documents(collection_name(ServiceTicket), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/inspiration", response_model=dict)
def create_inspiration(payload: Inspiration):
    try:
        _id = create_document(collection_name(Inspiration), payload)
        return {"id": _id, "message": "Inspiration veröffentlicht"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inspiration", response_model=List[dict])
def list_inspiration(tag: Optional[str] = None, limit: int = 50):
    try:
        f = {"tags": {"$in": [tag]}} if tag else {}
        return get_documents(collection_name(Inspiration), f, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
