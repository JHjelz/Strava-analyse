# 🚴‍♂️ Strava-analyse 🏃‍♀️

Dette prosjektet er en Python-klient for å koble seg opp mot [Strava sitt API](https://developers.strava.com/).  
Systemet lar deg autentisere med dine egne Strava-nøkler, hente tokens og bruke disse til å kjøre spørringer mot Strava-data (f.eks. aktiviteter).

## 📑 Innhold

- [✨ Funksjoner](#funksjoner)
- [⚙️ Krav](#krav)
- [🔧 Oppsett](#oppsett)
- [🔑 Autentisering mot Strava](#autentisering-mot-strava)
- [▶️ Bruk](#bruk)
- [📂 Struktur](#struktur)

---

## ✨ Funksjoner

- 💾 Lagrer og håndterer **Strava API-nøkler og tokens** lokalt.
- 🔄 Sørger for at **access_token alltid er gyldig** (automatisk fornyelse med refresh_token).
- 🚀 Enklere inngangspunkt via `StravaKlient`, som kan utvides med flere funksjoner (hente aktiviteter, segmenter osv.).

---

## ⚙️ Krav

- 🐍 Python 3.8+
- 📦 Biblioteker (installer med `pip install -r requirements.txt`):
  - `requests`

---

## 🔧 Oppsett

1. **Lag Strava API-tilgang**  
Gå til: [Strava API Settings](https://www.strava.com/settings/api)
Følg instruksjonene for hvordan du setter opp eget API.
Her finner du din `Client ID` og `Client Secret`.  
Sett opp et API med følgende redirect URI:
http://localhost

2. **Kopier dine nøkler inn i prosjektet**  
Første gang må du selv opprette filen `strava_tokens.json` i rotmappen. Den skal ligge i `.gitignore` slik at dine private nøkler aldri pushes til GitHub.
Kodene du må legge inn er:
- `client_id`
- `client_secret`
- `authorization_code` (se neste seksjon)

---

## 🔑 Autentisering mot Strava

Første gang må du hente en **authorization code** fra Strava:

1. 🌐 Åpne denne lenken i nettleseren, og erstatt `ID` med din `client_id`:
https://www.strava.com/oauth/authorize?client_id=ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read_all,activity:read_all

2. 🔓 Logg inn og trykk **Authorize**.

3. ↪️ Du blir videresendt til en ugyldig side, med en URL som ligner:
http://localhost/?state=&code=AUTHORIZATION_CODE&scope=read,activity:read_all,read_all

4. 📋 Kopier verdien fra `code=...`. Dette er din **authorization_code**.
Legg den inn i strava_tokens.json (se [Oppsett](#oppsett)).

⚠️ Viktig:
- `authorization_code` er en **engangskode** (kun gyldig én gang).
- Når du har brukt den første gang, får du `access_token` (kortvarig) og `refresh_token` (langvarig).
- Etter dette oppdateres tokens automatisk med refresh_token – du trenger aldri hente authorization_code igjen.

---

## ▶️ Bruk

Når `strava_tokens.json` er satt opp, kan du starte programmet:

```bash
python main.py
```

Ved oppstart vil systemet:

1. 📖 Lese dine nøkler fra `strava_tokens.json`.

2. ⏳ Hvis `access_token` mangler eller er utløpt → hente nytt token via Strava API.

3. 💾 Oppdatere `strava_tokens.json` med nye tokens.

## 📂 Struktur

Prosjektet er organisert slik:

```bash
STRAVA-ANALYSE/
│
├── main.py                # ▶️ Startpunkt – oppretter Strava-klient
├── privat.py              # 🔐 Klasse for håndtering av lokal token-fil
│
├── python/
│   ├── tilgang.py         # 🔄 Funksjoner for å hente/oppdatere tokens
│   └── strava.py          # 🚴 Strava-klient (inngangspunkt til API)
│
├── strava_tokens.json     # 🔑 Privat fil med API-nøkler og tokens (i .gitignore)
├── requirements.txt       # 📦 Avhengigheter
└── README.md              # 📑 Dokumentasjon
```
