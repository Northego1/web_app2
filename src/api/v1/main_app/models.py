from sqlalchemy import JSON, ForeignKey, Integer, String, PickleType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from main_logics.db.database import Base
from main_logics.schemas.schemeMap import Transport_type


class Routes(Base):
    __tablename__ = 'routes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    route_coords: Mapped[list] = mapped_column(PickleType, nullable=False)
    transport_type: Mapped[Transport_type] = mapped_column(String, nullable=False)
    rest_places: Mapped[dict] = mapped_column(JSON, nullable=True)

    route_owner = relationship('User', back_populates='') 