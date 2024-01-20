from typing import Dict, List, Union
from ..data import texts


class DataPrettifier:
    __all_redirects_template = texts.SHOW_REDIRECT_TEMPLATE

    def __repr__(self):
        return f"DataPrettifierObject - ({id(self)})"

    async def prettify_redirects_info(self, redirects: List[Dict[str, Union[str, int]]]) -> str:
        redirects_info = ""
        for redirect in redirects:
            redirects_info += self.__all_redirects_template.format(
                from_chat_name=redirect["copy_from_name"],
                from_chat_id=redirect["copy_from"],
                to_chat_name=redirect["copy_to_name"],
                to_chat_id=redirect["copy_to"],
            )
        return redirects_info
