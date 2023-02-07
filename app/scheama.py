from pydantic import BaseModel
from pydantic import ValidationError
from errors import HttpError

class CreateAdvertising(BaseModel):

    header: str
    description: str
    user: str


def validate_create_advertising(json_data):

    try:
        advertising_schema = CreateAdvertising(**json_data)
        return advertising_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())

