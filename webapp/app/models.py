from sqlalchemy import Column, Integer, String

from .database import Base


class Student(Base):
    __tablename__ = "estudantes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column("nome", String, nullable=False)
    nationality = Column("nacionalidade", String, nullable=False)
    generation = Column("geracao", String, nullable=False)
    accommodation = Column("acolhimento", String, nullable=False)

    institutional_accommodation = Column(
        "acolhimento_institucional",
        String(20),
        nullable=False,
        default="Não informado",
        server_default="Não informado",
    )