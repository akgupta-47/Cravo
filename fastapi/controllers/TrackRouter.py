from datetime import date
from uuid import uuid4
import shortuuid
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from database import get_db
from models.Order import Order as OrderModel
from models.Track import Track as TrackModel
from models.Feedback import Feedback as FeedbackModel
from utils import TrackUtils
from logger import logger

order_router = APIRouter(
    prefix='/track',
    tags=['Track']
)

def createNewTrack(order: OrderModel, db: AsyncSession = Depends(get_db)) -> TrackModel :
       new_track = TrackModel(id = str(shortuuid.uuid()),
                           order = order.id,
                           etam = TrackUtils.calculateEstimatedArrivalTime(order.address_id, order.shop_id))
       
       if new_track.id != None :
           return new_track