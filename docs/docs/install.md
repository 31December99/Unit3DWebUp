
# Installazione di Unit3DwebUp (Unit3Dwup) 

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


#### Configura tunnel ssh per raggiungere il backend remoto dal tuo browser locale

ssh -L 7000:localhost:7000 -L 8000:localhost:8000 utente_tuo_server@ip_del_tuo_server -N

Ora puoi collegarti al bot attraverso il browser all'indirizzo 127.0.0.1:8000



#### Installazione di unit3DwebUp con frontend and backend su differenti host

Installa solo il backend sul tuo server remoto
```
docker-compose up -d backend redis
```

Installa solo il frontend sulla tua macchina locale
```
docker run -d -p 8080:80 parzival2025/unit3dwebup_frontend:latest
```

Nota:
```
-p 8080(porta del tuo browser): 80 ( la porta fissa dentro il docker) 
```