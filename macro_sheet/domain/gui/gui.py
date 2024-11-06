from dataclasses import dataclass, field

from common.domain import Domain


@dataclass
class Gui(Domain):
    id: str
    name: str
    owner_id: str | None
    worksheet_id: str
    url: str
