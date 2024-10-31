from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.loop_block.loop_block import LoopBlock
from macro_sheet.domain.block.reference_block import ReferenceBlock
from macro_sheet.domain.Function.block_function import BlockFunction


@dataclass
class Worksheet(Domain):
    worksheet_id: str
    name: str
    owner_id: str | None
    blocks: list[Block] = field(default_factory=list)
