from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import Inventory
from app.schemas import InventoryItem, InventoryItemCreate, InventoryItemUpdate

router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"],
)

@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@router.post("/", response_model=InventoryItem)
def add_inventory(item: InventoryItemCreate, db: Session = Depends(get_db)):
    new_item = Inventory(name=item.name, count=item.count)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/{item_id}", response_model=InventoryItem)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=InventoryItem)
def update_inventory(item_id: int, item: InventoryItemUpdate, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(inventory_item, key, value)
    db.commit()
    return inventory_item

@router.delete("/{item_id}")
def delete_inventory(item_id: int, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(inventory_item)
    db.commit()
    return {"message": "Item deleted successfully"}