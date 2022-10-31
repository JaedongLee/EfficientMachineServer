from dataclasses import dataclass

from entity.ToolSourceAttributeEntity import ToolSourceAttributeEntity


class ToolSourceAttributeDTO:
    def __init__(self, entity: ToolSourceAttributeEntity):
        self.id = entity.Id
        self.tool_source_id = entity.ToolSourceId
        self.tool_id = entity.ToolId
        self.attribute_name = entity.AttributeName
        self.attribute_value = entity.AttributeValue
