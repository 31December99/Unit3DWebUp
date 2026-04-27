# Welcome to Unit3DwebUp docs 0.0.3

* [Github](https://github.com/31December99/Unit3DWebUp)

* [Demo video Here](https://streamable.com/agoizj)

* [Basato su Unit3dup](https://github.com/31December99/Unit3Dup)


* Wup nasce con un frontend e un backend

* Wup è installabile con un solo comando docker

* Wup frontend lo installi a casa o sullo stesso server del backend

* Wup è accessibile solo da locale oppure da remoto attraverso ssh

* Wup può essere installato come backend anche senza docker (ad esempio su server remoto senza sudo)

* Wup frontend è consigliabile installarlo con docker 

Funzioni attualmente implementate

* Scansiona cartelle e sottocartelle (livello 1)
* Crea uno o più torrents
* Crea automaticamente il titolo per la pagina del tracker facendo differenza tra movie e serie 
* Estrae screenshots
* Aggiunge un webp alla descrizione
* Aggiunge il link del trailer alla descrizione
* Cerca l'ID per TMDB, IMDB, TVDB
* Seeding in qBittorrent
* Ottiene mediainfo output per ogni video
* Carica uno o più torrents sul tracker

Funzioni non ancora testate ma presenti nella versione CLI

*    Estrae la prima pagina come cover da file PDF
*    Reseeding uno o più torrents
*    Seeding del torrent tra due O.S.
*    Assegna un titolo differente dall'originale a una stagione durante il caricamento
*    Windows

Funzioni non ancora testate ma presenti nella versione CLI

*    Genera meta-info per Games (IGDB)
*    Seeding in Transmission e rTorrent

## Installazione versione Docker

*    Configura Unit3Dwup utilizzando il file .env(example)
*    Rinominalo in .env
*    run docker-compose pull

## Come funziona
Il backend espone alcuni endpoints.

Per ogni file video, Unit3Dwup crea un job_id che corrisponde all’hash del suo percorso.

Una lista di job_id compone una job_list rappresentata nel frontend come un elenco di poster o locandine.

Per ogni pagina, Unit3Dwup crea un job_list_id che corrisponde all’hash del percorso principale scansionato

Un WebSocket è stato inizialmente creato per inviare aggiornamenti di avanzamento durante la creazione del file torrent

In un secondo momento per inviare i log di stato del server.

Al contrario della versione CLI tutto il processo non viene eseguito in uno solo step se non espressamente
richiesto:

### Pulsante scansiona

* Ricerca di file o cartelle
* Estrazione del titolo e ricerca su TMDb in base alla categoria, film o serie TV
* Ricerca su TVDB ed estrazione dell’id IMDb dal campo remote_ids
* Creazione degli screenshot e file webp
* Creazione della descrizione con MediaInfo

Una volta completato il processo di scansione otterrai un pagina di poster ognuno dei quali rappresenta 
un job_id sui cui lavorare.

### Cliccare su ogni locandina

***Cliccando su una o più locandine*** è possibile aggiornare alcuni dati:
 
* titolo
* TMDb/TVDB/IMDb IDs
* Link del poster (solo per frontend)

Per ogni poster è anche possibile creare il suo torrent, eseguire l’upload o avviare il seeding
Le tre opzioni dipendono dalla loro effettiva disponibilità in quanto non esiste una sequenza obbligata.
Ad esempio l'esistenza di un torrent creato il giorno prima permette di fare uploading o seeding.

A questo punto è possibile anche chiudere l’applicazione senza perdere i dati processati.

### Caricare tutto

Se invece vogliamo caricare tutta la pagina di torrents sul tracker dobbiamo cliccare sul pulsante "Carica"

Se elimini o aggiungi file nella cartella di scansione, devi cliccare nuovamente su “scan” per aggiornare la pagina

Verranno scansionati solo i nuovi file senza ripetere l'intero processo.