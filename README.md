# Startnummer-checker: Kustloop Vrouwenpolder

Controleert elke 5 minuten of er een startnummer beschikbaar komt op
https://platform.inschrijven.nl/2026090550469 en stuurt een e-mail
zodra dat het geval is. Draait gratis via GitHub Actions, 24/7, zonder
dat er iets op je eigen apparaat hoeft te draaien of open hoeft te staan.

Je krijgt alleen een mail op het moment dat de status omslaat van
"niet beschikbaar" naar "beschikbaar". Bij elke losse check zonder
wijziging (dus ook niet elke 5 minuten als er niets verandert) wordt
er geen mail verstuurd.

## Bestanden

- `check_ticket.py` — het controlescript
- `.github/workflows/check-ticket.yml` — de GitHub Actions workflow (elke 5 minuten)
- `state.txt` — wordt automatisch aangemaakt/bijgewerkt door het script, hoef je niet zelf aan te maken

## Installatie

1. Zet deze bestanden in een GitHub-repository, met behoud van de mapstructuur
   (`.github/workflows/check-ticket.yml` moet exact op dat pad staan).
2. Maak een Gmail app-wachtwoord aan via myaccount.google.com/apppasswords
   (vereist 2-staps-verificatie op je Google-account).
3. Zet in de repository-instellingen (Settings > Secrets and variables > Actions)
   de volgende 5 secrets:
   - `SMTP_SERVER` — bijv. `smtp.gmail.com`
   - `SMTP_PORT` — `587`
   - `SMTP_USERNAME` — je Gmail-adres
   - `SMTP_PASSWORD` — het zojuist aangemaakte app-wachtwoord
   - `EMAIL_TO` — het adres waar de melding naartoe moet
4. Test de workflow één keer handmatig via het tabblad "Actions" > "Check
   startnummer beschikbaarheid" > "Run workflow".

## Let op

- Ik ben er niet honderd procent zeker van of de gratis GitHub Actions-minuten
  bij een private repository voor jouw account toereikend zijn; controleer dit
  zelf op je GitHub-instellingenpagina. Bij een publieke repository is dit
  onbeperkt en gratis.
- GitHub garandeert het interval van 5 minuten niet exact; tijdens drukte op
  GitHub kan er vertraging optreden.
- Als inschrijven.nl ooit de opzet van de pagina wijzigt, kan de check
  onopgemerkt stoppen met werken. Check daarom af en toe ook zelf de pagina.
