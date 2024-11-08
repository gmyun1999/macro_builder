from dataclasses import dataclass, field

from common.domain import Domain


@dataclass
class Gui(Domain):
    id: str
    name: str
    url: str


@dataclass
class Script(Domain):
    """
    gui 에 들어가는 스크립트.
    """

    id: str
    script_code: str
    gui_id: str
    script_hash: str
