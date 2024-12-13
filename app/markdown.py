from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List


class TaskKind(Enum):
    CHECKBOX_FILLED  = auto()
    CHECKBOX_EMPTY   = auto()
    WARNING      = auto()
    EMERGENCY    = auto()

class MdKind(Enum):
    HR_RULE = auto()
    TABLE   = auto()
    QUOTE   = auto()
    LIST    = auto()
    TASK    = auto()
    HEADING = auto()
    STYLING = auto()

@dataclass
class MdHeading:
    level: int
    content: str

@dataclass
class MdHrRule:
    kind: int

@dataclass
class MdTable:
    headers: List[str]
    rows: List[List[str]]

@dataclass
class MdQuote:
    level: int
    content: str

@dataclass
class MdList:
    items: List[str]

@dataclass
class MdTask:
    kind: int
    description: str

@dataclass
class MdGallery:
    style: str
    content: str

@dataclass
class MdStyling:
    style: str
    content: str

@dataclass
class MdTag:
    kind: MdKind
    heading: Optional[MdHeading] = None
    hr_rule: Optional[MdHrRule] = None
    table: Optional[MdTable] = None
    quote: Optional[MdQuote] = None
    list: Optional[MdList] = None
    task: Optional[MdTask] = None
    styling: Optional[MdStyling] = None

