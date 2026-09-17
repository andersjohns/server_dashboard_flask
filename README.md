# Raspberry Pi Serverdashboard med Flask og Waitress

Dette er et Flask-prosjekt som viser status på en Raspberry Pi/Linux-server.

Dashboardet viser blant annet:

- CPU-bruk
- minnebruk
- diskplass
- temperatur
- oppetid

Alle elevens webprosjekter skal ligge i:

```text
/home/elev/www/
```

Prosjektet skal derfor få denne plasseringen:

```text
/home/elev/www/server_dashboard_flask/
```

---

## 1. Kontroller nødvendige programmer

Python 3 og Git er installert i Raspberry Pi OS fra før. 

Kontroller installasjonene:

```bash
python3 --version
git --version
python3 -m pip --version
```
Installer det som eventuelt mangler:

```bash
sudo apt update
sudo apt install python3-venv python3-pip git -y
```
---

## 2. Opprett `www`-mappen

Opprett mappen dersom den ikke finnes, og gå inn i den:

```bash
mkdir -p /home/elev/www
cd /home/elev/www
```

Kontroller plasseringen:

```bash
pwd
```

Resultatet skal være:

```text
/home/elev/www
```

---

## 3. Hent prosjektet

Velg alternativ A eller B.

### Alternativ A – klon fra GitHub

Stå i `/home/elev/www/` og klon repositoriet:

```bash
cd /home/elev/www
git clone https://github.com/BRUKERNAVN/server_dashboard_flask.git
cd server_dashboard_flask
```

Bytt ut URL-en med adressen til riktig repository.


---
## 3.1 Feil med rettigheter

Kontroller hvem du er, og hvem som eier mappene:

```bash
whoami
ls -ld /home/elev/www
ls -ld /home/elev/www/server_dashboard_flask
```

Hvis `root` eier `www`-mappen eller prosjektet, kan brukeren `elev` få `Permission denied`. Gi da brukeren eierskap:

```bash
sudo chown -R elev:elev /home/elev/www
chmod -R u+rwX /home/elev/www
```
eller 

```bash
sudo chown -R elev:elev /home/elev/www/server_dashboard_flask
chmod -R u+rwX /home/elev/www/server_dashboard_flask

```
- `chown` endrer hvem som eier filene og mappene.
- `chmod` endrer hvilke rettigheter eieren har.

Ikke bruk `chmod -R 777`. Ikke bruk `sudo` når du oppretter `.venv`, installerer pakker i `.venv` eller starter Waitress.

Hvis `.venv` ble opprettet av feil bruker eller kopiert fra Windows, kan det opprettes på nytt:

```bash
cd /home/elev/www/server_dashboard_flask
rm -r .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Kontroller alltid `pwd` før du sletter en mappe.


### Alternativ B – fork prosjektet på GitHub

En **fork** lager en kopi av lærerens repository på elevens egen GitHub-konto. Eleven kan dermed endre prosjektet og pushe endringene til sitt eget repository uten å endre lærerens original.

1. Åpne lærerens repository på GitHub.
2. Trykk **Fork** øverst til høyre.
3. Velg elevens egen GitHub-konto som eier.
4. Behold repository-navnet eller gi kopien et nytt navn.
5. Trykk **Create fork**.
6. Åpne den nye forken på elevens GitHub-konto.
7. Trykk **Code** og kopier HTTPS-adressen.

Klon deretter elevens egen fork til Raspberry Pi:

```bash
cd /home/elev/www
git clone https://github.com/ELEVENS_BRUKERNAVN/server_dashboard_flask.git
cd server_dashboard_flask
```

Kontroller hvilket repository prosjektet er koblet til:

```bash
git remote -v
```

Adressen ved `origin` skal vise elevens eget GitHub-brukernavn. Etter endringer kan eleven pushe til sin egen fork:

```bash
git status
git add .
git commit -m "Oppdaterte serverdashboardet"
git push
```

Hvis læreren senere oppdaterer originalprosjektet, kan eleven åpne sin fork på GitHub og bruke **Sync fork** for å hente inn de nyeste endringene. Deretter kjøres:

```bash
cd /home/elev/www/server_dashboard_flask
git pull
```

> **Fork og clone er ikke det samme:** Fork lager en GitHub-kopi under elevens konto. Clone laster et repository ned til Raspberry Pi.

---

## 4. Opprett et virtuelt Python-miljø

Stå i prosjektmappen:

```bash
cd /home/elev/www/server_dashboard_flask
```

Opprett miljøet med Raspberry Pi OS sin Python 3:

```bash
python3 -m venv .venv
```

Aktiver miljøet:

```bash
source .venv/bin/activate
```

Når miljøet er aktivert, vises ofte `(.venv)` først på kommandolinjen.

Kontroller at `python` peker inn i `.venv`:

```bash
which python
python --version
python -m pip --version
```

Vi bruker `python3` når miljøet opprettes. Etter aktivering bruker vi `python`, fordi denne kommandoen da peker på Python inne i `.venv`.

---

## 5. Installer pakkene

Oppgrader først `pip` inne i miljøet:

```bash
python -m pip install --upgrade pip
```

Installer pakkene fra `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Hvis prosjektet mangler `requirements.txt`, installer minst Flask og Waitress:

```bash
python -m pip install flask waitress
```

Kontroller at pakkene er installert:

```bash
python -m pip show flask waitress
```

---

## 6. Test med Flasks utviklingsserver

```bash
python app.py
```

Denne kommandoen fungerer når `app.py` inneholder:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Dette starter Flasks utviklingsserver. Den er beregnet på utvikling og testing, ikke permanent serverdrift.

På selve Raspberry Pi kan den normalt åpnes på:

```text
http://127.0.0.1:5000
```

Stopp utviklingsserveren med `Ctrl+C`.

Flask kan alternativt startes med:

```bash
python -m flask --app app run --debug
```

---

## 7. Start appen med Waitress

Waitress brukes når løsningen skal kjøres mer stabilt og være tilgjengelig fra andre maskiner i nettverket:

```bash
waitress-serve --listen=0.0.0.0:8080 app:app
```

Forklaring:

| Del | Betydning |
|---|---|
| `waitress-serve` | starter Waitress |
| `--listen=0.0.0.0:8080` | lytter på alle nettverkskort på port 8080 |
| første `app` | filen `app.py`, uten `.py` |
| andre `app` | Flask-variabelen `app` |

Finn Raspberry Pi-ens IP-adresse:

```bash
hostname -I
```

Åpne dashboardet fra en PC i samme nettverk:

```text
http://RASPBERRY_PI_IP:8080
```

Eksempel:

```text
http://10.200.14.66:8080
```

Stopp Waitress med `Ctrl+C`.

---

## 8. Åpne brannmuren hvis UFW brukes

```bash
sudo ufw allow 8080/tcp
sudo ufw status
```

Kontroller at Waitress lytter på port 8080:

```bash
ss -tulpn | grep 8080
```

Test lokalt på Raspberry Pi:

```bash
curl http://127.0.0.1:8080
```

---

## 9. Feil med rettigheter

Kontroller hvem du er, og hvem som eier mappene:

```bash
whoami
ls -ld /home/elev/www
ls -ld /home/elev/www/server_dashboard_flask
```

Hvis `root` eier `www`-mappen eller prosjektet, kan brukeren `elev` få `Permission denied`. Gi da brukeren eierskap:

```bash
sudo chown -R elev:elev /home/elev/www
chmod -R u+rwX /home/elev/www
```

- `chown` endrer hvem som eier filene og mappene.
- `chmod` endrer hvilke rettigheter eieren har.

Ikke bruk `chmod -R 777`. Ikke bruk `sudo` når du oppretter `.venv`, installerer pakker i `.venv` eller starter Waitress.

Hvis `.venv` ble opprettet av feil bruker eller kopiert fra Windows, kan det opprettes på nytt:

```bash
cd /home/elev/www/server_dashboard_flask
rm -r .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Kontroller alltid `pwd` før du sletter en mappe.

---

## 10. Temperatur på Raspberry Pi

Temperaturen leses med:

```bash
vcgencmd measure_temp
```

Hvis kommandoen ikke fungerer, kan pakken installeres med:

```bash
sudo apt install libraspberrypi-bin -y
```

---

## 11. Starte prosjektet senere

```bash
cd /home/elev/www/server_dashboard_flask
source .venv/bin/activate
waitress-serve --listen=0.0.0.0:8080 app:app
```

Avslutt det virtuelle miljøet når du er ferdig:

```bash
deactivate
```

---

## 12. Oppdatere et klonet prosjekt

Stopp først serveren med `Ctrl+C`. Kjør deretter:

```bash
cd /home/elev/www/server_dashboard_flask
git pull
source .venv/bin/activate
python -m pip install -r requirements.txt
waitress-serve --listen=0.0.0.0:8080 app:app
```

---

## 13. Forslag til elevoppgaver

1. Legg til visning av IP-adresse.
2. Legg til visning av klokkeslett.
3. Legg til fargevarsel hvis CPU-bruk er over 80 %.
4. Legg til fargevarsel hvis diskbruk er over 80 %.
5. Lag en egen side `/status`.
6. Start prosjektet med Waitress.
7. Test dashboardet fra en annen PC.
8. Lag en systemd-tjeneste slik at dashboardet starter automatisk.

---

## 14. Eksempel på systemd-tjeneste

Opprett tjenestefilen:

```bash
sudo nano /etc/systemd/system/dashboard.service
```

Innhold:

```ini
[Unit]
Description=Flask Serverdashboard med Waitress
After=network.target

[Service]
User=elev
Group=elev
WorkingDirectory=/home/elev/www/server_dashboard_flask
ExecStart=/home/elev/www/server_dashboard_flask/.venv/bin/waitress-serve --listen=0.0.0.0:8080 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Last inn tjenestefilen og aktiver tjenesten:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard
sudo systemctl status dashboard
```

Etter endringer kan tjenesten startes på nytt:

```bash
sudo systemctl restart dashboard
sudo systemctl status dashboard
```

Se de siste loggmeldingene:

```bash
journalctl -u dashboard -n 50 --no-pager
```

---

## Huskelapp

```bash
cd /home/elev/www/server_dashboard_flask
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
waitress-serve --listen=0.0.0.0:8080 app:app
```
