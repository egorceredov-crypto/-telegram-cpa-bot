# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
#
# from database.models import YandexPrice
#
#
# async def orm_add_yandex(session: AsyncSession, model_num: int, name: str, price: float, link: str):
#     obj = await session.get(YandexPrice, model_num)
#
#     if obj:
#         obj.model_name = name
#         obj.price = price
#         obj.partner_link = link
#     else:
#         new_obj = YandexPrice(
#             model_number=model_num,
#             model_name=name,
#             price=price,
#             partner_link=link
#         )
#         session.add(new_obj)
#
#     await session.commit()
#
# async def orm_get_yandex_price(session: AsyncSession, model_num: int):
#     query = select(YandexPrice).where(YandexPrice.model_number == model_num)
#     result = await session.execute(query)
#     return result.scalar_one_or_none()
