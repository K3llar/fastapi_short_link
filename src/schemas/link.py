from typing import Optional

from pydantic import UUID4, AnyHttpUrl, BaseModel, Field


class LinkBase(BaseModel):
    original_link: Optional[AnyHttpUrl] = Field(None)
    short_link: Optional[str] = Field(max_length=16, default='')
    number_of_uses: Optional[int]


class LinkCreate(BaseModel):
    original_link: AnyHttpUrl
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
