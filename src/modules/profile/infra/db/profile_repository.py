from typing import List

from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.profile.infra.db.tables import profile_table
from src.modules.user.domain.types import TUserId


class ProfileRepository(IProfileRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, profile: Profile) -> None:
        self.session.add(profile)

    async def save(self, profile: Profile) -> None:
        await self.session.commit()

    async def delete(self, profile: Profile) -> None:
        await self.session.delete(profile)

    async def find_by_user_id(self, user_id: TUserId) -> Profile | None:
        return await self.session.get(Profile, user_id)

    async def get_next_profile(
        self,
        rank: int,
        user_id: int,
        ages: List[int],
        city: str,
        sex: Sex,
        interest: Sex | None = None,
        skip_current: bool = True,
    ) -> Profile | None:
        stmt = (
            select(Profile)
            .where(profile_table.c.city == city)
            .where(profile_table.c.age.in_(ages))
            .where(profile_table.c.is_active == True)
            .order_by(profile_table.c.rank.desc(), profile_table.c.user_id.desc())
            .limit(1)
        )

        if interest:
            stmt = stmt.where(profile_table.c.sex == interest)
            stmt = stmt.where(profile_table.c.interest == sex)
        else:
            stmt = stmt.where(profile_table.c.interest == None)

        if rank and user_id:
            if skip_current:
                stmt = stmt.where(
                    tuple_(profile_table.c.rank, profile_table.c.user_id)
                    < tuple_(rank, user_id)
                )
            else:
                stmt = stmt.where(
                    tuple_(profile_table.c.rank, profile_table.c.user_id)
                    <= tuple_(rank, user_id)
                )

        result = await self.session.execute(stmt)
        return result.scalars().first()
