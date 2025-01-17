from pydantic import BaseModel

class InventoryItemBase(BaseModel):
    name: str
    quantity: int

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True