from pydantic import BaseModel

class BookCreate(BaseModel):
    titulo: str
    autor: str
    editorial: str
    publicadoEn: int
    categoria: str

class BookResponse(BookCreate):
    id: int

# NUEVO: Estructura para los préstamos y devoluciones
class LoanRequest(BaseModel):
    userId: int
    inventoryNumber: str