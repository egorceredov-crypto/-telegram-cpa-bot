# from sqlalchemy import Float, String, Integer, DateTime, func
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#
#
# class Base(DeclarativeBase):
#     created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
#     updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
#
#
# class YandexPrice(Base):
#     __tablename__ = 'yandex_prices'
#
#     model_number: Mapped[int] = mapped_column(Integer, primary_key=True)
#
#     model_name: Mapped[str] = mapped_column(String(), nullable=False)
#
#     price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
#
#     partner_link: Mapped[str] = mapped_column(String(), nullable=False)
