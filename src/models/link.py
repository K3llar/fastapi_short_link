from fastapi_users_db_sqlalchemy.guid import GUID

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text

from src.core.db import Base


class Link(Base):
    __tablename__ = 'Links'
    link_id = Column(Integer, primary_key=True)
    original_link = Column(Text(), nullable=False, index=True)
    short_link = Column(String(16), nullable=False, unique=True)
    is_private = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    user_id = Column(GUID, ForeignKey('user.id'), default=None)
    number_of_uses = Column(Integer, default=0)
