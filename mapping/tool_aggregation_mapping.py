from typing import List

from dto.ToolAggregationDTO import ToolAggregationDTO
from entity.ToolEntity import ToolEntity
from entity.ToolSourceAttributeEntity import ToolSourceAttributeEntity
from entity.ToolSourceEntity import ToolSourceEntity


def to_dtos(tool_entities: List[ToolEntity], tool_source_entities: List[ToolSourceEntity],
            tool_source_attribute_entities: List[ToolSourceAttributeEntity]) -> List[ToolAggregationDTO]:
    tool_aggregation_dtos = []
    for tool_entity in tool_entities:
        tool_id = tool_entity.Id
        matched_tool_source_entity = None
        for tool_source_entity in tool_source_entities:
            if tool_id == tool_source_entity.ToolId:
                matched_tool_source_entity = tool_source_entity
                break
        if matched_tool_source_entity is None:
            tool_aggregation_dtos.append(ToolAggregationDTO(tool_entity, None, None))
            continue
        tool_source_id = matched_tool_source_entity.Id
        matched_tool_source_attribute_entities = []
        for tool_source_attribute_entity in tool_source_attribute_entities:
            if tool_source_attribute_entity.ToolSourceId == tool_source_id:
                matched_tool_source_attribute_entities.append(tool_source_attribute_entity)
        tool_aggregation_dtos.append(
            ToolAggregationDTO(tool_entity, matched_tool_source_entity, matched_tool_source_attribute_entities))
    return tool_aggregation_dtos


def dtos_to_dicts(tool_aggregation_dtos: List[ToolAggregationDTO]):
    tool_aggregation_dicts = []
    for tool_aggregation in tool_aggregation_dtos:
        tool_aggregation_dict = tool_aggregation.__dict__
        tool_aggregation_dicts.append(tool_aggregation_dict)
        tool_aggregation_dict['tool'] = tool_aggregation.tool.__dict__
        tool_aggregation_dict['tool_source'] = tool_aggregation.tool_source.__dict__
        tool_source_dict = tool_aggregation_dict['tool_source']
        tool_source_attributes = tool_source_dict['attributes']
        if len(tool_source_attributes) > 0:
            tool_source_attribute_dicts = []
            for tool_source_attribute in tool_source_attributes:
                tool_source_attribute_dicts.append(tool_source_attribute.__dict__)
            tool_source_dict['attributes'] = tool_source_attribute_dicts
    return tool_aggregation_dicts
