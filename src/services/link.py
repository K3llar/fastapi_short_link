import random
import re

from sqlalchemy.ext.asyncio import AsyncSession

from . import constants as cst
from ..models import Link


def get_unique_short_link(symbols=cst.SYMBOLS,
                          length=cst.LEN_SHORT_URL):
    url_link = ''
    for char in range(length):
        url_link += random.choice(symbols)
    return


def regex_validation(string):
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
