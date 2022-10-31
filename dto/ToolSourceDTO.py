from dataclasses import dataclass
from typing import List

from dto.ToolSourceAttributeDTO import ToolSourceAttributeDTO
from entity.ToolSourceAttributeEntity import ToolSourceAttributeEntity
from entity.ToolSourceEntity import ToolSourceEntity


class ToolSourceDTO:
    def __init__(self, entity: ToolSourceEntity, attribute_entities: List[ToolSourceAttributeEntity]):
        self.id = entity.Id
        self.tool_id = entity.ToolId
        self.type = entity.Type
        self.homepage = entity.Homepage
        self.url_for_release = entity.URLForRelease
        self.release_asset_regex = entity.ReleaseAssetRegex
        if attribute_entities is None:
            return
        attribute_dtos = []
        for attribute_entity in attribute_entities:
            attribute_dto = ToolSourceAttributeDTO(attribute_entity)
            attribute_dtos.append(attribute_dto)
        self.attributes = attribute_dtos
