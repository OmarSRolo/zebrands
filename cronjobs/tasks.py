from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from project import app
from rest_framework.serializers import ValidationError


@app.task(bind=True)
def send_email(self, email_data: dict):
    try:
        msg_plain = render_to_string("email/" + email_data["template"], email_data["context"])

        email = EmailMessage(
            email_data["subject"],
            body=msg_plain,
            from_email=email_data["from_email"],
            to=email_data["to_email"]
        )

        if 'attachment' in email_data:
            file_path = email_data['attachment'][0]
            with open(file_path, 'rb') as file:
                email.attach(file_path.split('/')[-1], file.read(), 'application/pdf')

        email.content_subtype = "html"
        try:
            email.send()
        except Exception as e:
            raise ValidationError({"complete": True, "message": {"exception": [str(e)]}})
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10, max_retries=5)
