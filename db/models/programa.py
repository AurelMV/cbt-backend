from typing import Optional

from sqlmodel import SQLModel, Field


class ProgramaEstudios(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombrePrograma: str = Field(index=True)
