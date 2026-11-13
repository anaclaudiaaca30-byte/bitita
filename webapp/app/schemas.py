from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    nationality: str = Field(..., min_length=1, max_length=120)
    generation: str = Field(..., min_length=1, max_length=50)
    accommodation: str = Field(..., min_length=1, max_length=50)

    institutional_accommodation: Literal[
        "Sim", "Não", "Não informado"
    ] = "Não informado"


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