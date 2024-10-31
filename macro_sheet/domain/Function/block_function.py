from dataclasses import dataclass, field

from common.domain import Domain
from macro_sheet.domain.block.block import Block


@dataclass
class BlockFunction(Domain):
    id: str
    owner_id: str
    name: str
    blocks: list[Block] = field(default_factory=list)
    # 남이 만든 function을 가져오면 function을 복제한다음 owner_id만 바꾸면될듯.
