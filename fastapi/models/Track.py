from sqlmodel import SQLModel, Field
from datetime import datetime
import enum 

class StatusEnum(enum.Enum):
    PENDING = 'pending'
    PLACED = 'placed'
    ACCEPTED = 'accepted'
    FAILED = 'failed'
    OTW = 'on_the_way'
    REACHED = 'reached'
    DELIVERED = 'delivered'
    
class TrackBase(SQLModel):
    status: StatusEnum
    order_id: str
    rider_id: str
    etam: int # estimated time of arrival in minutes
    profile_id: str
    shop_id: str
    created_at: datetime = Field(default=datetime.UTC)
    
class Track(TrackBase, table=True):
    id = str = Field(default=None, primary_key=True)
    