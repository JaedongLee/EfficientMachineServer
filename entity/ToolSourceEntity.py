from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class ToolSourceEntity(declarative_base()):
    __tablename__ = "ToolSource"

    Id = Column(Integer, primary_key=True)
    Type = Column(String)
    URLForRelease = Column(String)
    ToolId = Column(Integer)
    Homepage = Column(String)
    ReleaseAssetRegex = Column(String)

