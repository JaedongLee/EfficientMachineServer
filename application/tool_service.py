from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database_init import engine
from dto.ToolAggregationDTO import ToolAggregationDTO
from dto.ToolDTO import ToolDTO
from entity.ToolEntity import ToolEntity
from entity.ToolSourceAttributeEntity import ToolSourceAttributeEntity
from entity.ToolSourceEntity import ToolSourceEntity
from enumation.ToolStatusEnum import ToolStatusEnum
from mapping import tool_aggregation_mapping


def list_usable_tool_aggregation() -> List[ToolAggregationDTO]:
    session = Session(engine)

    # 查询工具列表
    tool_query_stmt = select(ToolEntity).where(ToolEntity.Status.in_([ToolStatusEnum.USABLE.value]))
    tool_entities = []
    tool_ids = []
    for tool_entity in session.scalars(tool_query_stmt):
        tool_entities.append(tool_entity)
        tool_ids.append(tool_entity.Id)

    # 查询工具来源列表
    tool_source_query = select(ToolSourceEntity).where(ToolSourceEntity.ToolId.in_(tool_ids))
    tool_source_entities = []
    tool_source_ids = []
    for tool_source_entity in session.scalars(tool_source_query):
        tool_source_entities.append(tool_source_entity)
        tool_source_ids.append(tool_source_entity.Id)

    # 查询工具来源属性列表
    tool_source_attribute_query = select(ToolSourceAttributeEntity).where(ToolSourceAttributeEntity.ToolSourceId.in_(
        tool_source_ids))
    tool_source_attribute_entities = []
    for tool_source_attribute_entity in session.scalars(tool_source_attribute_query):
        tool_source_attribute_entities.append(tool_source_attribute_entity)

    # 构建工具聚合体
    tool_aggregation = tool_aggregation_mapping.to_dtos(tool_entities, tool_source_entities,
                                                        tool_source_attribute_entities)

    return tool_aggregation


def get_tool_by_tool_name(tool_name):
    session = Session(engine)
    tool_query_stmt = select(ToolEntity).where(ToolEntity.Name.is_(tool_name))
    tool_entity = session.scalar(tool_query_stmt)
    return ToolDTO(tool_entity)
