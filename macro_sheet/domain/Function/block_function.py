from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.block.block import Block


@dataclass
class BlockFunction(Domain):
    id: str
    owner_id: str
    name: str
    blocks: list[Block] = field(default_factory=list)
