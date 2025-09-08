MAPPING = {
    "properties":
        {
            "file_name": {
                "type": "keyword"
            },
            "creation_data": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ssXXX||EEE MMM dd HH:mm:ss Z yyyy"
            },
            "last_modified_date": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ssXXX||EEE MMM dd HH:mm:ss Z yyyy"
            },
            "size_in_bytes": {
                "type": "long"
            },
            "size_in_mb": {
                "type": "float"
            },
            "type": {
                "type": "text"
            },
            "media_type": {
                "type": "text"
            },
            "text": {
                "type": "text"
            }

        }
}