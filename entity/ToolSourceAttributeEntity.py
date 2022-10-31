from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class ToolSourceAttributeEntity(declarative_base()):
    __tablename__ = "ToolSourceAttribute"

    Id = Column(Integer, primary_key=True)
    ToolSourceId = Column(Integer)
    ToolId = Column(Integer)
    AttributeName = Column(String)
    AttributeValue = Column(String)
