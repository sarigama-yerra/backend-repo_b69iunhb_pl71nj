"""
Database Schemas for LIVARO Home

Jede Pydantic-Klasse entspricht einer Collection in MongoDB.
Der Collection-Name ist der kleingeschriebene Klassenname.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Account(BaseModel):
    vorname: str = Field(..., description="Vorname")
    nachname: str = Field(..., description="Nachname")
    email: EmailStr = Field(..., description="E-Mail-Adresse")
    telefon: Optional[str] = Field(None, description="Telefonnummer")
    rolle: str = Field("kunde", description="Rolle im System")
    marketing_opt_in: bool = Field(False, description="Einwilligung Marketing")

class Plan(BaseModel):
    account_email: EmailStr = Field(..., description="Zuordnung über E-Mail des Accounts")
    titel: str = Field(..., description="Titel des Plans")
    beschreibung: Optional[str] = Field(None, description="Beschreibung")
    status: str = Field("in_planung", description="Status des Plans")
    budget: Optional[float] = Field(None, ge=0, description="Budget in EUR")

class Angebot(BaseModel):
    plan_id: Optional[str] = Field(None, description="Referenz auf Plan")
    titel: str = Field(..., description="Titel des Angebots")
    preis: float = Field(..., ge=0, description="Preis in EUR")
    gueltig_bis: Optional[datetime] = Field(None, description="Gültig bis")
    status: str = Field("entwurf", description="Status")

class Beratung(BaseModel):
    account_email: EmailStr = Field(..., description="Zuordnung über E-Mail des Accounts")
    thema: str = Field(..., description="Beratungsthema")
    nachricht: Optional[str] = Field(None, description="Nachricht/Details")
    bevorzugter_termin: Optional[str] = Field(None, description="Terminpräferenz ISO-String")

class ServiceTicket(BaseModel):
    account_email: EmailStr = Field(..., description="Zuordnung über E-Mail des Accounts")
    kategorie: str = Field(..., description="Kategorie")
    beschreibung: str = Field(..., description="Beschreibung")
    prioritaet: str = Field("normal", description="Priorität")
    status: str = Field("offen", description="Status")

class Inspiration(BaseModel):
    titel: str = Field(..., description="Titel")
    tags: List[str] = Field(default_factory=list, description="Tags")
    bild_url: Optional[str] = Field(None, description="Bild-URL")
    beschreibung: Optional[str] = Field(None, description="Beschreibung")
