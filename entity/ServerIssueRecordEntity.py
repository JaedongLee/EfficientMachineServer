from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class ServerIssueRecordEntity(declarative_base()):
    __tablename__ = "ServerIssueRecord"

    Id = Column(Integer, primary_key=True)
    Type = Column(String)
    Stage = Column(String)
    ToolId = Column(Integer)
    ToolName = Column(String)
    IssueMessage = Column(String)

