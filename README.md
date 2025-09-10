# MUEZZIN-DATA-PROJECT
### -- A data pipline of consuming analyzing and saving data from audio files --


## Components
- **metadata**: Load all the file paths from a specific folder and extracts all the metadata on each file, then send it (kafka)
- **consumer_es_mongo**: Retrieve the metadata (kafka), and first index the metadata and save the files and ID to mongo, then in a different thread (so we wont get collusions) the service sends (kafka) the file path and id to the STT service and gets back (kafka) the transcribed text with id to add the text to the index in es 
- **speech_to_text**: Retrieve (kafka) a payload with a files path and id, transcribes the audio of the .bat file, adds the text to the payload and sends it back (kafka).
- **text_analyzer**: Analyzes the text via ES 
- **api**: Endpoints to retrieve data from es


## Notes:
*Flow-decision-1* I chose to index and save to mongo before transcribing because if we would transcribe before saving to mongo and indexing, we would get delays indexing and saving which we prior to be quick.

*Flow-decision-2* I sent the path straight to stt because i did not see the reason to take the file from mongo and send that file to transcribing when i already have a path that i could send directly.

*Analyzing-calculations* 
- 1 The calculation of the percentage is 'total words' \ 'found word' - on less_threatening_words the words count are cut by half before calculating
- 2 The classification of the danger level is calculated based on the percent and the amount of word found together, i chose not to use the percentage alone because we used it already for checking if is_bds is True/False, and could be a situation with a lot of words so the % is low and then we will want to check the words count alone


## Outer Containers used
- **Apache Kafka**: Message broker for asynchronous communication between services
- **MongoDB**: Document database for storing the audio files with a unique id
- **Elasticsearch**: Indexes the data for easy search
- **Kibana**: UI for tracking indexes in es


## project structure
```
├─ services/
│ ├─ metadata/
│ │ ├─ app/ # file discovery + metadata extraction + Kafka producer
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
│ ├─ consumer_es_mongo/
│ │ ├─ app/ # Kafka consumer -> ES indexer + Mongo writer + sending to STT
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
│ ├─ speech_to_text/
│ │ ├─ app/ # STT worker: consumes jobs, emits transcripts
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
│ ├─ text_analyzer/
│ │ ├─ app/ # Retrieving text from es and adding text analyzin as 'text-metadata'
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
├─ api/
│ │ ├─ app/ # Endpoints to retrieve data from es
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
├─ docker-compose.yml
├─ .gitignore
└─ README.md
```

## Quick Start

The easiest way to run the entire system using Docker Compose:

```bash
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### thing i would change/add if i had more time:
- Seperate the es and mongo to different services
- Send the metadata to es, mongo and stt in different topics so if one service is down the other can still work
- find a way to send automatically to analyzer after transcribing
- more endpoints for searching and mongo retrieving