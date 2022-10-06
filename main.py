from typing import Dict, Optional
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Custom model
    """

    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    """
    Custom model - Update
    """

    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory: Dict[int, str] = {}


@app.get("/get-item/{item_id}")
def get_item_by_id(
    item_id: int = Path(None, description="The ID of the item you'd like to view.")
):
    """
    Get a particular item, default item_id to None
    """
    return inventory[item_id]


# http://127.0.0.1:8000/get-by-name/1?name=Milk
@app.get("/get-by-name/{item_id}")
def get_item_by_query_parameter(item_id: int, name: Optional[str] = None):
    """
    Query parameters
    """
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=400, detail="Item ID already exists")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    """
    Post method
    """
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="Item ID already exists.")

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    """
    Route to update the val of the existing items
    """
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    if item.name:
        inventory[item_id].name = item.name

    if item.price:
        inventory[item_id].price = item.price

    if item.brand:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete")):
    """
    Delete an item
    """
    if item_id not in inventory:
        raise HTTPException(
            status_code=404, detail="Item ID already exists or was never there."
        )

    del inventory[item_id]
