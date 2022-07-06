"""
Sem ideia do que colocar aqui.
"""
import smtplib
from fastapi import FastAPI
# pylint: disable=no-name-in-module
from pydantic import BaseModel

app = FastAPI()


class EmailBody(BaseModel):
    """
    _summary_
    """
    from_email: str
    password: str
    text: str
    subject: str
    to_email: str
    email_to_send: int


@app.get("/")
async def root():
    """
    _summary_
    """
    return {"message": "Hello World"}


@app.post("/send-email")
async def send_email(request: EmailBody):
    """_summary_
    """
    try:
        smtp_obj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(request.from_email, request.password)

    # pylint: disable=invalid-name
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        smtp_obj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

    message = f"""From: {request.from_email}\n
    To: {request.to_email}\nSubject: {request.subject}\n\n{request.text}"""

    try:
        for email in range(request.email_to_send):
            smtp_obj.sendmail(request.from_email, request.to_email,
                              message)
    except smtplib.SMTPDataError as error:
        return {"message": f"Error: {error}"}

    return {"message": "Email sent"}
