from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class ToolEntity(declarative_base()):
    __tablename__ = "Tool"

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    RuntimeEnvironment = Column(String)
    ReleaseType = Column(String)
    MainProgramLocation = Column(String)
    Description = Column(String)
    Status = Column(String)
    FileName = Column(String)
    CreatedDate = Column(String)
    LastUpdatedDate = Column(String)
    Version = Column(String)

