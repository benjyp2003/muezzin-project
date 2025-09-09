# MUEZZIN-DATA-PROJECT
### -- A data pipline of consuming analyzing and saving data from audio files --


## Components
- **metadata**: Load all the file paths from a specific folder and extracts all the metadata on each file, then send it (kafka)
- **consumer_es_mongo**: Retrieve the metadata (kafka), and first index the metadata and save the files and ID to mongo, then in a different thread (so we wont get collusions) the service sends (kafka) the file path and id to the STT service and gets back (kafka) the transcribed text with id to add the text to the index in es 
- **speech_to_text**: Retrieve (kafka) a payload with a files path and id, transcribes the audio of the .bat file, adds the text to the payload and sends it back (kafka).
### notes:
*1.* I chose to index and save to mongo before transcribing because if we would transcribe before saving to mongo and indexing, we would get delays indexing and saving which we prior to be quick.

*2.* I did not see the reason to take the file from mongo and send that file to transcribing when i already have a path that i could send directly.

### Containers needed
- **Apache Kafka**: Message broker for asynchronous communication between services
- **MongoDB**: Document database for storing the audio files with a unique id
- **Elasticsearch**: Indexes the data for easy search
- **Kibana**: UI for tracking indexes in es


