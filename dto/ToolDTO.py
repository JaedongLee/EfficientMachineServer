from dataclasses import dataclass

from entity.ToolEntity import ToolEntity


class ToolDTO:
    def __init__(self, entity: ToolEntity):
        self.id = entity.Id
        self.name = entity.Name
        self.runtime_environment = entity.RuntimeEnvironment
        self.release_type = entity.ReleaseType
        self.main_program_location = entity.MainProgramLocation
        self.description = entity.Description
        self.status = entity.Status
        self.file_name = entity.FileName
        self.created_date = entity.CreatedDate
        self.last_updated_date = entity.LastUpdatedDate
        self.version = entity.Version
        self.file_extension_name = entity.FileExtensionName

