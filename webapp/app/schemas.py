from pydantic import BaseModel, ConfigDict, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    nationality: str = Field(..., min_length=2, max_length=120)
    generation: str = Field(..., min_length=2, max_length=50)
    accommodation: str = Field(..., min_length=2, max_length=50)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DashboardItem(BaseModel):
    label: str
    value: int
