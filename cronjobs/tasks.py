from core.services.EmailService import EmailService, BasicEmail
from project import app


@app.task(bind=True)
def send_email(self, email_data: dict):
    email_data_struct: BasicEmail = BasicEmail(subject=email_data["subject"], template=email_data["template"],
                                               from_email=email_data["from_email"], to_email=email_data["to_email"],
                                               context=email_data["context"], message="")
    try:
        EmailService.send_email(email_data_struct)
    except Exception as e:
        print(e)
        return False
