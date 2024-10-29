from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.Function.function_block import FunctionBlock


@dataclass
class Worksheet(Domain):
    worksheet_id: str
    name: str
    owner_id: str | None
    blocks: list[FunctionBlock] = field(default_factory=list)
