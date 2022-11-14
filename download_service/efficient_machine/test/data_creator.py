from download_service.efficient_machine.util.download.DownloadInfo import DownloadInfo
from dto.ToolAggregationDTO import ToolAggregationDTO
from entity.ToolEntity import ToolEntity
from entity.ToolSourceEntity import ToolSourceEntity


def create_ditto_tool_aggregation():
    tool_entity = ToolEntity()
    tool_entity.Id = 1
    tool_entity.Name = 'Ditto'
    tool_entity.Status = 'Usable'
    tool_entity.FileName = 'DittoPortable_64bit_3_24_238_0.zip'
    tool_entity.Version = '3.24.238.0'
    tool_entity.ReleaseType = 'Portable'
    tool_source_entity = ToolSourceEntity()
    tool_source_entity.Id = 1
    tool_source_entity.URLForRelease = 'https://api.github.com/repos/sabrogden/Ditto/releases/latest'
    tool_source_entity.ToolId = 1
    tool_source_entity.ReleaseAssetRegex = 'DittoPortable_64bit.*.zip'
    tool_source_entity.Type = 'Github'
    tool_aggregation_dto = ToolAggregationDTO(tool_entity, tool_source_entity, [])
    return tool_aggregation_dto


def create_ditto_download_info():
    return DownloadInfo(
        'https://github.com/sabrogden/Ditto/releases/download/3.24.238.0/DittoPortable_64bit_3_24_238_0.zip',
        'DittoPortable_64bit_3_24_238_0',
        '3.24.238.0',
        'D:\\OneDrive\\Project\\Self\\EfficientMachine\\Service/download_service/resource/tool_program/Ditto',
        'D:\\OneDrive\\Project\\Self\\EfficientMachine\\Service/download_service/resource/tool_program/Ditto/DittoPortable_64bit_3_24_238_0.zip',
        'zip')

