import uuid
from sqlalchemy import INTEGER, Column, ForeignKey, String, Enum, Integer
import enum
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
    


class EidosEnum(enum.Enum):
    komodia = 'komodia'
    peripeteia = 'peripeteia'
    scifi = 'scifi'
    koinwniko = 'koinwniko'
    thriller = 'thriller'
    paidiko = 'paidiko'

   
def generate_uuid():
    return str(uuid.uuid4())

class DVD(Base):
    __tablename__ = "dvd"
    id : Mapped[str] = mapped_column(String(256), nullable=False, primary_key=True, default=generate_uuid)
    titlos : Mapped[str]  = mapped_column(String(256), nullable=False)
    eidos :Mapped[EidosEnum] = mapped_column(Enum(EidosEnum))
    temaxia: Mapped[int] = mapped_column(Integer, default = 0)

    def to_dict(self):
        return {"id": self.id, "titlos": self.titlos, "eidos": self.eidos.value, "temaxia": self.temaxia}
    
    def to_dict2(self):
        return {"id": self.id, "titlos": self.titlos, "eidos": self.eidos, "temaxia": self.temaxia}

