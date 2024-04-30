from dataclasses import dataclass, asdict
from typing import Tuple

from django.core.mail import send_mail
from django.template.loader import render_to_string


@dataclass
class BasicEmail:
    subject: str
    template: str
    from_email: str
    to_email: list[str]
    message: str
    context: dict[str, str]
    attachment: Tuple[bytes, str] = None

    def as_dict(self) -> dict:
        email_dict = {
            "subject": self.subject,
            "template": self.template,
            "from_email": self.from_email,
            "to_email": self.to_email,
            "message": self.message,
            "context": self.context,
        }
        if self.attachment:
            email_dict["attachment"] = self.attachment
        return email_dict


class EmailService:
    @staticmethod
    def send_email(email_data: BasicEmail):
        msg_plain = render_to_string("email/" + email_data.template, email_data.context)
        send_mail(email_data.subject, message="", from_email=email_data.from_email,
                  recipient_list=email_data.to_email, html_message=msg_plain)
