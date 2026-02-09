from __future__ import annotations

import smtplib
import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import cast

from flask import current_app


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    user: str
    password: str
    support_email: str

    @staticmethod
    def from_flask_config() -> "SMTPConfig":
        smtp_host = current_app.config.get("SMTP_HOST")
        smtp_port = current_app.config.get("SMTP_PORT", 587)
        smtp_user = current_app.config.get("SMTP_USER")
        smtp_password = current_app.config.get("SMTP_PASSWORD")
        support_email = current_app.config.get("SUPPORT_EMAIL")

        missing: list[str] = []
        if not isinstance(smtp_host, str) or not smtp_host.strip():
            missing.append("SMTP_HOST")
        if not isinstance(smtp_user, str) or not smtp_user.strip():
            missing.append("SMTP_USER")
        if not isinstance(smtp_password, str) or not smtp_password.strip():
            missing.append("SMTP_PASSWORD")
        if not isinstance(support_email, str) or not support_email.strip():
            missing.append("SUPPORT_EMAIL")

        if missing:
            raise RuntimeError(
                f"Missing SMTP configuration: {', '.join(missing)}. "
                f"Check your .env and that load_dotenv() is called."
            )

        return SMTPConfig(
            host=cast(str, smtp_host),
            port=int(smtp_port),
            user=cast(str, smtp_user),
            password=cast(str, smtp_password),
            support_email=cast(str, support_email),
        )


class EmailService:
    @staticmethod
    def send_email(user_email: str, subject: str, text: str) -> None:

        cfg = SMTPConfig.from_flask_config()
        msg = EmailService._build_message(
            sender_email=cfg.user,
            to_email=user_email,
            subject=subject,
            user_email=user_email,
            text=text,
        )
        EmailService._send(cfg, msg)

    @staticmethod
    def send_to_support(user_email: str, subject: str, text: str) -> None:
        cfg = SMTPConfig.from_flask_config()
        msg = EmailService._build_message(
            sender_email=cfg.user,
            to_email=cfg.support_email,
            subject=subject,
            user_email=user_email,
            text=text,
        )
        EmailService._send(cfg, msg)

    @staticmethod
    def _build_message(
        *,
        sender_email: str,
        to_email: str,
        subject: str,
        user_email: str,
        text: str,
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = f"Bank App <{sender_email}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        body = f"""
        <h3>Support Request</h3>
        <p><b>From:</b> {user_email}</p>
        <p>{text}</p>
        """
        msg.attach(MIMEText(body, "html"))
        return msg

    @staticmethod
    def _send(cfg: SMTPConfig, msg: MIMEMultipart) -> None:
        context = ssl.create_default_context()

        if cfg.port == 465:
            with smtplib.SMTP_SSL(
                cfg.host, cfg.port, timeout=20, context=context
            ) as server:
                server.login(cfg.user, cfg.password)
                server.send_message(msg)
            return

        with smtplib.SMTP(cfg.host, cfg.port, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(cfg.user, cfg.password)
            server.send_message(msg)
