from typing import Dict, Optional, Union
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID

class Test(BaseModel):
    id: Optional[Union[str, UUID]] = None
    title: str
    content: str
    published: bool
      
    class Config:
        from_attributes = True
    