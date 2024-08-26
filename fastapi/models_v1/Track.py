from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Enum
import enum 

class StatusEnum(enum.Enum):
    PENDING = 'pending'
    PLACED = 'placed'
    ACCEPTED = 'accepted'
    FAILED = 'failed'
    OTW = 'on_the_way'
    REACHED = 'reached'
    DELIVERED = 'delivered'

class Track(Base):
    __tablename__ = "track"

    id = Column(String,primary_key=True,nullable=False)
    status = Column(Enum(StatusEnum),nullable=False, server_default='PENDING')
    order = Column(String,nullable=False)
    rider = Column(String,nullable=False)
    etam = Column(String,nullable=False) # Estimated time to arrival in minutes
    profile_id = Column(String,nullable=False)
    shop = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
