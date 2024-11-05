from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.block.block import Block


@dataclass
class Worksheet(Domain):
    id: str
    name: str
    owner_id: str | None
    main_blocks: list[Block]
    blocks: list[Block] = field(default_factory=list)
