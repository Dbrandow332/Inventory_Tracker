from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import InventoryItem
from app.schemas import InventoryItem, InventoryItemCreate

router = APIRouter()

@router.post("/inventory/", response_model=InventoryItem)
def create_inventory_item(item: InventoryItemCreate, db: Session = Depends(get_db)):
    db_item = InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/inventory/{item_id}", response_model=InventoryItem)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/inventory/{item_id}")
def del_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": f"User with ID {item_id} has been deleted successfully"}