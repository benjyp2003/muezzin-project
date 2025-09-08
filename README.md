# MUEZZIN-PROJECT


### Components

- **metadata**: Loads all the file paths from a specific folder and extracts all the metadata on each file
- **speech_to_text**: Consumes all the metadata from the previous service and transcribes the audio from the files to text, adds the text as a new field to the message and sends it via kafka 
- **consumer_es_mongo**: Consumes the data from the STT service indexes all the data into elasticsearch, and stores the binary .wav files with a unique id in MongoDB


### Containers needed
- **Apache Kafka**: Message broker for asynchronous communication between services
- **MongoDB**: Document database for storing the audio files with a unique id
- **Elasticsearch**: Indexes the data for easy search
- **Kibana**: UI for tracking indexes in es


