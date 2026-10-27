from fastapi import APIRouter, HTTPException, Path, Query, Response 
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

FAKE_DB: dict[int, dict] = {}

@router.get("", response_model=list[ItemRead])
def list_items(
    skip : int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None, 
    disponible: bool | None = None, 
): 
    resultats = []

#creer une sorte de tuples 

    for item in FAKE_DB.values():

        if q is not None and q.lower() not in item["titre"].lower():
            continue 

        if disponible is not None and item["disponible"] != disponible: 
            continue 

        #item passe les filtres 

        resultats.append(item)

    return resultats[skip : skip + limit]


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None: 
        raise HTTPException(status_code = 404, detail=f"Item {item_id} introuvable")
    return item 


@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1 
    return item 

@router.put("/{item_id}", response_model=ItemRead)
def put_item(payload: ItemCreate, item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(
            status_code=404, detail = f"Item {item_id} introuvable"
        )
    updated_item = {"id": item_id, **payload.model_dump()}
    FAKE_DB[item_id] = updated_item
    return updated_item

@router.patch("/{item_id}", response_model=ItemRead)
def patch_item(payload: ItemUpdate, item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB : 
        raise HTTPException( status_code=404, detail=f"Item {item_id} introuvable"
        )

    stored_item = FAKE_DB[item_id]
    update_data = payload.model_dump(exclude_unset=True)
    stored_item.update(update_data)

    FAKE_DB[item_id] = stored_item
    return stored_item

@router.delete("/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException( status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]