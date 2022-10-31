from dataclasses import dataclass
from typing import List

from dto.ToolDTO import ToolDTO
from dto.ToolSourceDTO import ToolSourceDTO
from entity.ToolEntity import ToolEntity
from entity.ToolSourceAttributeEntity import ToolSourceAttributeEntity
from entity.ToolSourceEntity import ToolSourceEntity


class ToolAggregationDTO:
    def __init__(self, tool_entity: ToolEntity, tool_source_entity: ToolSourceEntity,
                 tool_source_attribute_entities: List[ToolSourceAttributeEntity]):
        self.tool = ToolDTO(tool_entity)
        if tool_source_entity is None:
            return
        self.tool_source = ToolSourceDTO(tool_source_entity, tool_source_attribute_entities)
