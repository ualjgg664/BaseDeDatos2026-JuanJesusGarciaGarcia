import logging
from fastapi import APIRouter, Depends, HTTPException, status
from mysql.connector.abstracts import MySQLConnectionAbstract
from database import get_db
from models import LoanRequest

router = APIRouter()
logger = logging.getLogger("uvicorn")

# POST /loans - Crea un nuevo préstamo
@router.post("/")
async def create_loan(loan: LoanRequest, conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor()
    try:
        # Insertamos el registro con los nombres exactos de tu tabla
        cursor.execute(
            "INSERT INTO Prestamo (idUsuario, numeroInventario, fechaPrestamo) VALUES (%s, %s, CURDATE())",
            (loan.userId, loan.inventoryNumber)
        )
        conn.commit()
        return {"message": "Préstamo creado con éxito"}
    except Exception as e:
        conn.rollback()
        logger.exception("Error al crear préstamo")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al procesar el préstamo: {str(e)}"
        )

# POST /loans/return - Devuelve un ejemplar
@router.post("/return")
async def return_loan(loan: LoanRequest, conn: MySQLConnectionAbstract = Depends(get_db)):
    cursor = conn.cursor()
    try:
        # Eliminamos el préstamo usando los nombres exactos de tu tabla
        cursor.execute(
            "DELETE FROM Prestamo WHERE idUsuario = %s AND numeroInventario = %s",
            (loan.userId, loan.inventoryNumber)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No se encontró un préstamo activo con esos datos"
            )
        
        conn.commit()
        return {"message": "Ejemplar devuelto con éxito"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        logger.exception("Error al devolver préstamo")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error al procesar la devolución: {str(e)}"
        )