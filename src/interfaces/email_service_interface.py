from abc import ABC, abstractmethod
from typing import List


class IEmailService(ABC):
    @abstractmethod
    def send_email(self, to: List[str], template_name: str, params=None, attachments=None) -> str:
        """Interface Method"""

    def _parse_template_body(self):
        print("Parsing template body...")
