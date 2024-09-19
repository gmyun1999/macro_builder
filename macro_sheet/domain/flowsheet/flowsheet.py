from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.worksheet import Worksheet


@dataclass
class Workflow(Domain):
    workflow_id: str
    name: str
    worksheets: list[Worksheet] = field(default_factory=list)
