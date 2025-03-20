import smtplib
from pydantic import EmailStr
from rabbit.config import settings
from email.message import EmailMessage
from pydantic import EmailStr

def create_order_confirmation_template(
    order_id: int,
    total_cost: int,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Вы оформили заказ"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Поздравляю, вы оформили заказ</h1>
            Цвяточки уже едут к вам!
            ID заказа - {order_id} на cумму {total_cost}
        """,
        subtype="html"
    )
    return email


def done_order_confirmation_template(
    order_id: int,
    total_cost: int,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Ваш заказ доставлен"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Ваш заказ доставлен</h1>
            ID заказа - {order_id} на cумму {total_cost}
        """,
        subtype="html"
    )
    return email


def send_order_confirmation_email(
        order_id: int,
        total_cost: int,
        email_to: EmailStr,
):
    msg_content = create_order_confirmation_template(order_id=order_id,
                                               total_cost=total_cost,
                                               email_to= email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
        print(f"Письмо о заказе отправлено на почту пользователю {email_to}")


def send_done_order_confirmation_email(
        order_id: int,
        total_cost: int,
        email_to: EmailStr,
):
    msg_content = done_order_confirmation_template(order_id=order_id,
                                               total_cost=total_cost,
                                               email_to= email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
        print(f"Письмо о заказе отправлено на почту пользователю {email_to}")