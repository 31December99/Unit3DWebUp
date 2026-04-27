
## Installazione di Unit3DwebUp (Unit3Dwup)

unit3dwebUp ( abbreviato unit3dwup..) può essere installato sulla tua macchina oppure in remoto solo se chiudi
le porte 8080 e 8000

l'app non è ancora provvista di una pagina di login e puo funzionare in locale oppure in remoto via SSH

*** Le porte 8080 e 8000 devono essere chiuse dal firewall se install l'app su un server. *** TODO

*** Non installare l'app se non chiudi le porte ***

Per installare wup devi scaricare questi due file e configurare ssh:

* scarica il file [.env(example)](https://raw.githubusercontent.com/31December99/Unit3DwebUp/master/.env(example))
* scarica il file di installazione [docker-compose.yml](https://raw.githubusercontent.com/31December99/Unit3DwebUp/master/docker-compose.yml)

* Salva il file `docker-compose.yml` e `.env(example)` in una cartella a piacere ad esempio unit3dwup 
* entra nella cartella unit3dwup
* Configura il file `.env.example`
* rinominalo in  `.env`

Scarica l'immagine docker

```bash
docker-compose pull
```

Avvia il backend

```bash
ENVPATH=/percorso/del_tuo/file_env docker compose up
```
Ora puoi collegarti attraverso il browser all'indirizzo http://127.0.0.1:8080/


### Configura tunnel ssh per raggiungere l'app quando viene installa su server remoto

*** Le porte 8080 e 8000 devono essere chiuse dal firewall sul tuo server***
 

```ssh -L 8000:127.0.0.1:8000 utente_tuo_server@ip_del_tuo_server -N```

Ora puoi collegarti attraverso il browser all'indirizzo http://127.0.0.1:8080/


### Installazione del solo Backend

Se vuoi installare solo il backend e richiamarlo attraverso il tuo frontend puoi farlo con o senza docker

```bash
ENVPATH=/percorso/del_tuo/file_env docker compose up backend
```

### Installazione del solo Backend senza docker

Installa redis

* sudo apt install redis-server -y
* sudo nano /etc/redis/redis.conf
* assicurati che siano presenti queste stringhe: 
  * 'bind 127.0.0.1 -::1'
  * 'protected-mode yes'
  * 'appendonly yes'
  * 'daemonize yes'

Installa il backend

```bash
pip install Unit3DwebUp
```

Set il percorso del tuo file .env (senza il file .env)

export ENVPATH=/home/parzival

RUN

```bash
uvicorn unit3dwup.start:app
```