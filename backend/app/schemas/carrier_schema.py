from pydantic import BaseModel


class CarrierBase(BaseModel):
    carrier_code: str
    name: str
    has_webhook: bool = False
    metadata: dict | None = None


class CarrierCreate(CarrierBase):
    pass


class CarrierResponse(CarrierBase):
    id: int

    class Config:
        orm_mode = True
