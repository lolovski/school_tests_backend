from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Class(Base):
    __tablename__ = 'class'
    name: Mapped[str] = mapped_column(String(64))

    users: Mapped[List['User']] = relationship(
        'User',
        back_populates='class_',
        cascade='all',
        lazy='selectin'
    )
    

"""    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}"""