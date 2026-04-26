## Installare Redis su ultra.cc senza sudo

* wget https://download.redis.io/redis-stable.tar.gz

* tar xzf redis-stable.tar.gz

* cd redis-stable

* make

### Configura redis

- cd redis-stable
- nano redis.conf
    - verifica che sia presente la stringa "bind 127.0.0.1"
    - ctrl-o per salvare
    - ctrl-x per uscire da nano
- cd src
- [non lanciare redis senza specificare il file di configurazione]
- ./redis-server ../redis.conf --daemonize yes

#### Test Redis server

- ./redis-cli ping

#### Shutdown Redis server

Nel caso servisse chiudere redis

- ./redis-cli -p 7000 shutdown

## Test veloce di connessione a Redis lato client

- nc 127.0.0.1 7000
- ping -> il server deve rispondere PONG


#### Installazione Docker

- sudo apt update
- sudo apt install docker.io docker-compose -y
- sudo systemctl enable --now docker
- docker --version
- docker-compose --version

## Run docker senza sudo

- sudo usermod -aG docker $USER
- newgrp docker
- riavvia sessione