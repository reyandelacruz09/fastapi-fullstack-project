from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..models import Address, City
from ..database import SessionLocal
from .auth import get_current_user

templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
    prefix='/addresses',
    tags=['addresses']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class AddressRequest(BaseModel):
    street: str
    city_id: int
    province_id: int


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/address-page")
async def render_address_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        addresses = db.query(Address).filter(Address.user_id == user.get("id")).all()

        return templates.TemplateResponse("address.html", {
            "request": request,
            "addresses": addresses,
            "user": user
        })

    except:
        return redirect_to_login()


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_addresses(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    addresses = db.query(Address)\
        .join(City)\
        .filter(Address.user_id == user.get('id'))\
        .all()

    result = []
    for addr in addresses:
        result.append({
            "id": addr.id,
            "street": addr.street,
            "city": addr.city.name,
            "province": addr.city.province.name
        })

    return result


@router.get("/{address_id}", status_code=status.HTTP_200_OK)
async def read_address(user: user_dependency, db: db_dependency, address_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    addr = db.query(Address)\
        .join(City)\
        .filter(Address.id == address_id)\
        .filter(Address.user_id == user.get('id'))\
        .first()

    if addr is None:
        raise HTTPException(status_code=404, detail='Address not found')

    return {
        "id": addr.id,
        "street": addr.street,
        "city": addr.city.name,
        "province": addr.city.province.name
    }


@router.post("/")
async def create_address(user: user_dependency, db: db_dependency, request: AddressRequest):

    city = db.query(City).filter(City.id == request.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    if city.province_id != request.province_id:
        raise HTTPException(status_code=400, detail="City does not belong to province")

    address = Address(
        street=request.street,
        city_id=request.city_id,
        user_id=user.get("id")
    )

    db.add(address)
    db.commit()


@router.put("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(
    user: user_dependency,
    db: db_dependency,
    address_request: AddressRequest,
    address_id: int = Path(gt=0)
):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    address = db.query(Address)\
        .filter(Address.id == address_id)\
        .filter(Address.user_id == user.get('id'))\
        .first()

    if address is None:
        raise HTTPException(status_code=404, detail='Address not found')

    city = db.query(City).filter(City.id == address_request.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    address.street = address_request.street
    address.city_id = address_request.city_id

    db.add(address)
    db.commit()


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(user: user_dependency, db: db_dependency, address_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    address = db.query(Address)\
        .filter(Address.id == address_id)\
        .filter(Address.user_id == user.get('id'))\
        .first()

    if address is None:
        raise HTTPException(status_code=404, detail='Address not found')

    db.query(Address)\
        .filter(Address.id == address_id)\
        .filter(Address.user_id == user.get('id'))\
        .delete()

    db.commit()
