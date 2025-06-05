from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.Track import Track as TrackModel

async def commit_new_track(db: AsyncSession, track : TrackModel) -> TrackModel :
    try:
        db.add(track)  # Stage the track for insertion
        await db.commit()  # Commit transaction
        await db.refresh(track)  # Refresh the instance to get DB-generated values
        return track  # Return the persisted track
    except Exception as e:
        raise e

async def get_track_by_id(db: AsyncSession, track_id: str) -> Optional[TrackModel]:
    """Fetch a single track by its ID."""
    stmt = select(TrackModel).filter(TrackModel.id == track_id)
    result = await db.execute(stmt)
    return result.scalars().first()  # Fetch the first matching track or None