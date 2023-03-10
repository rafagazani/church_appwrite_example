from pydantic import BaseModel


class ChurchModel(BaseModel):
    name: str
    fantasyName: str
    cpfCnpj: str
    status: bool
    zipCode: str
    city: str
    uf: str
    district: str
    street: str
    number: str
    complement: str = None
    contact: str = None
    email: str = None
    phone1: str
    phone2: str = None
    facebook: str = None
    instagram: str = None
    youtube: str = None
    site: str = None
    tiktok: str = None
    churchHeadId: str = None
    responsibleId: str

