from typing import Optional

from pydantic import BaseModel, Field, UUID4, AnyUrl


class LinkBase(BaseModel):
    original_link: Optional[AnyUrl] = Field(None)
    short_link: Optional[str] = Field(None, min_length=1, max_length=16)
    number_of_uses: Optional[int]


class LinkCreate(BaseModel):
    original_link: str = Field(..., min_length=1, max_length=255)
    short_link: Optional[str] = Field(max_length=16, default='')
    is_private: Optional[bool] = Field(default=False)


class LinkUpdate(LinkBase):
    is_private: Optional[bool]


class LinkDB(LinkBase):
    link_id: int
    is_private: Optional[bool]
    is_hidden: Optional[bool]
    user_id: Optional[UUID4]

    class Config:
        orm_mode = True


