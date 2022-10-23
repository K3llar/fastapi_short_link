from pydantic import UUID4, AnyHttpUrl, BaseModel, Field


class LinkBase(BaseModel):
    original_link: AnyHttpUrl | None = Field(None)
    short_link: str | None = Field(max_length=16, default='')
    number_of_uses: int | None


class LinkCreate(BaseModel):
    original_link: AnyHttpUrl
    short_link: str | None = Field(max_length=16, default='')
    is_private: bool | None = Field(default=False)


class LinkUpdate(BaseModel):
    is_private: bool | None


class LinkDB(LinkBase):
    link_id: int
    is_private: bool | None
    is_hidden: bool | None
    user_id: UUID4 | None

    class Config:
        orm_mode = True
