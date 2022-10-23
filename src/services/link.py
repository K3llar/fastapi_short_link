import random
import re

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Link
from . import constants as cst


def get_unique_short_link(
        symbols=cst.SYMBOLS,
        length=cst.LEN_SHORT_URL) -> str:
    url_link = ''.join(random.choice(symbols)
                       for _ in range(length))
    return url_link


def regex_validation(string) -> bool:
    if re.match(cst.PATTERN, string):
        return True
    return False


async def increase_counter(
        link_obj: Link,
        session: AsyncSession
) -> None:
    count = int(link_obj.number_of_uses)
    link_obj.number_of_uses = count + 1
    session.add(link_obj)
    await session.commit()
    await session.refresh(link_obj)
