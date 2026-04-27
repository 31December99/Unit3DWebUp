
# Installazione di Unit3DwebUp (Unit3Dwup) su macchina locale (no server)

Per installare wup devi scaricare questi due file e configurare ssh:

* scarica il file [.env(example)](https://raw.githubusercontent.com/31December99/Unit3DwebUp/master/.env(example))
* scarica il file di installazione [docker-compose.yml](https://raw.githubusercontent.com/31December99/Unit3DwebUp/master/docker-compose.yml)

* Salva il file `docker-compose.yml` e `.env(example)` in una cartella a piacere ad esempio unit3dwup 
* entra nella cartella unit3dwup
* Configura il file `.env.example`
* rinominalo in  `.env`

Ora crea una variabile ambiente (una)

* `export ENVPATH=/il_percorso/del/tuo_file_env`
* Run docker-compose:

```bash
docker-compose pull
docker-compose up
```
Ora puoi collegarti attraverso il browser all'indirizzo http://127.0.0.1:8080/


