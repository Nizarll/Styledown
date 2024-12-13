from dataclasses import dataclass
from typing import List
from app.markdown import MdLink

@dataclass
class Env:
    files: List[MdLink]
