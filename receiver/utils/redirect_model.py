from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Redirect:
    id: int = None
    copy_to: Union[int, str] = None
    copy_to_name: str = None
    copy_from: Union[int, str] = None
    copy_from_name: str = None

    def to_dict(self) -> Dict:
        return self.__dict__

