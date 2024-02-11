from ..config.settings import settings
from typing import Final, Dict, Union
import requests


class SenderAPIController:
    __SERVICE_API_LINK: Final[str] = settings.SENDER_API

    def _execute_api_post_request(self, post_request_link: str) -> Dict:
        api_url: str = self.__SERVICE_API_LINK + post_request_link
        return requests.post(api_url).json()

    """
                                CRUD
    """

    def create_redirect(self, copy_from: Union[int, str], copy_to: Union[int, str]) -> Dict:
        post_request_link: str = f"/add_redirect/{copy_from}_{copy_to}"
        return self._execute_api_post_request(post_request_link)

    def read_all_redirects(self) -> Dict:
        post_request_link: str = "/get_all_redirects"
        return self._execute_api_post_request(post_request_link)

    def update_redirect(self, redirect_id: int, copy_from: Union[int, str], copy_to: Union[int, str]) -> Dict:
        post_request_link: str = f"/update_redirect/{redirect_id}_{copy_from}_{copy_to}"
        return self._execute_api_post_request(post_request_link)

    def delete_redirect(self, redirect_id: int) -> Dict:
        post_request_link: str = f"/remove_redirect/{redirect_id}"
        return self._execute_api_post_request(post_request_link)

    def delete_all_redirects(self) -> Dict:
        post_request_link: str = f"/remove_all_redirects"
        return self._execute_api_post_request(post_request_link)

    """
                                EXTRA
    """

    def copy_history(self, copy_from: Union[int, str], copy_to: Union[int, str]) -> Dict:
        post_request_link: str = f"/copy_history/{copy_from}_{copy_to}"
        return self._execute_api_post_request(post_request_link)

    def is_valid_chat(self, chat_id: Union[str, int]) -> Dict:
        post_request_link: str = f"/validate/{chat_id}"
        return self._execute_api_post_request(post_request_link)
