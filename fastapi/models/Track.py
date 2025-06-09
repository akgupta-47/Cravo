from database import Base
from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
import enum


class StatusEnum(enum.Enum):
    PENDING = "pending"
    PLACED = "placed"
    ACCEPTED = "accepted"
    FAILED = "failed"
    OTW = "on_the_way"
    REACHED = "reached"
    DELIVERED = "delivered"


class Track(Base):
    __tablename__ = "track"

    id = Column(String, primary_key=True, nullable=False)
    status = Column(
        ENUM(StatusEnum, name="statusenum", create_type=False),
        nullable=False,
        server_default=text("'pending'::statusenum"),
    )
    order = Column(String, ForeignKey("orders.id"), nullable=False)
    rider = Column(String, nullable=False)
    etam = Column(String, nullable=False)  # Estimated time to arrival in minutes
    profile_id = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
