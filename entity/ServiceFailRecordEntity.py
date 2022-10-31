from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class ServiceIssueRecordEntity(declarative_base()):
    __tablename__ = "ServiceIssueRecord"

    Id = Column(Integer, primary_key=True)
    Type = Column(String)
    Stage = Column(String)
    ToolId = Column(Integer)
    ToolName = Column(String)
    IssueMessage = Column(String)

