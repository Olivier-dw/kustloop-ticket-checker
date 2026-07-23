import os
import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
import urllib.request

URL = "https://platform.inschrijven.nl/2026090550469"
STATE_FILE = "state.txt"
MARKER = "geen startnummers beschikbaar"
SANITY_CHECK = "kustloop"


def fetch_page(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (ticket-checker; persoonlijk gebruik)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def is_available(html: str) -> bool:
    text = html.lower()
    return MARKER not in text


def read_last_state() -> str:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return "unknown"


def write_state(state: str) -> None:
    with open(STATE_FILE, "w") as f:
        f.write(state)


def send_email(subject: str, body: str) -> None:
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USERNAME"]
    smtp_pass = os.environ["SMTP_PASSWORD"]
    email_to = os.environ["EMAIL_TO"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email_to

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [email_to], msg.as_string())


def main() -> None:
    try:
        html = fetch_page(URL)
    except Exception as e:
        print(f"Ophalen van de pagina is mislukt, sla deze check over: {e}")
        sys.exit(0)

    if SANITY_CHECK not in html.lower():
        print("Paginainhoud zag er onverwacht uit, sla deze check over ter voorkoming van foutmeldingen.")
        sys.exit(0)

    available = is_available(html)
    last_state = read_last_state()
    print(f"Status nu: {'beschikbaar' if available else 'niet beschikbaar'} | vorige status: {last_state}")

    # Belangrijk: er wordt uitsluitend een mail verstuurd bij de OVERGANG
    # van 'niet beschikbaar' naar 'beschikbaar'. Bij een ongewijzigde status
    # (ook als die 'beschikbaar' blijft, of bij elke losse check) wordt er
    # geen mail verstuurd. Zo krijg je nooit een mail per check, alleen
    # op het moment dat er daadwerkelijk een nieuw startnummer verschijnt.
    if available and last_state != "available":
        send_email(
            subject="Startnummer beschikbaar: Kustloop Vrouwenpolder",
            body=(
                "Er lijkt een startnummer beschikbaar te zijn op het doorverkoopplatform.\n\n"
                f"Link: {URL}\n\n"
                f"Gecheckt op (UTC): {datetime.now(timezone.utc).isoformat()}\n\n"
                "Let op: dit is een automatische check op basis van tekst op de pagina. "
                "Controleer de pagina zelf voordat je conclusies trekt of contact opneemt met de verkoper."
            ),
        )
        print("E-mail verstuurd.")

    write_state("available" if available else "unavailable")


if __name__ == "__main__":
    main()
