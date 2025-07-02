# Strava-analyse

Dette er Python-kode til å koble opp mot Strava sitt API. Lag ditt eget API og bruk dine personlige nøkler til å kjøre spørringer i systemet.

## Bruk

Info om å lage ditt eget Strava API: https://developers.strava.com/docs/getting-started/

Gå til lenken: https://www.strava.com/settings/api. Her finner du din ID, Client Secret med mer.

Bruk følgende lenke i nettleseren din med den gitte client_id:
https://www.strava.com/oauth/authorize?client_id=ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read_all,activity:read_all

Du vil da komme til en side hvor du trykker 'Authorize'.
Du kommer så til en side som ikke eksisterer med lenke lik den under:
http://localhost/?state=&code=authCode&scope=read,activity:read_all,read_all

Her må du kopiere AUTHORIZATION_CODE.