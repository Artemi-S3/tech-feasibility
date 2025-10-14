import os
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from models import ItemIn, ItemOut

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
)
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class ItemORM(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)

class PostgresBackend:
    def connect(self) -> None:
        Base.metadata.create_all(engine)

    def list_all(self, limit: Optional[int]) -> List[ItemOut]:
        with SessionLocal() as db:
            q = db.query(ItemORM).order_by(ItemORM.id.asc())
            if limit:
                q = q.limit(limit)
            rows = q.all()
            return [ItemOut(id=str(r.id), name=r.name, path=r.path) for r in rows]

    def create_item(self, item: ItemIn) -> ItemOut:
        with SessionLocal() as db:
            row = ItemORM(name=item.name, path=item.path)
            db.add(row)
            db.commit()
            db.refresh(row)
            return ItemOut(id=str(row.id), name=row.name, path=row.path)

    def close(self) -> None:
        pass
