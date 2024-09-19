from abc import ABC
from dataclasses import dataclass, field
from enum import StrEnum

from common.domain import Domain


class BlockType(StrEnum):
    CONTROL = "CONTROL"
    CONDITION = "CONDITION"
    ACTION = "ACTION"


@dataclass
class Block(Domain, ABC):
    block_type: BlockType = field(init=False)
