from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    college_company: str
    stream: str
    experience: str


class CandidateResponse(CandidateCreate):
    id: int

    class Config:
        from_attributes = True