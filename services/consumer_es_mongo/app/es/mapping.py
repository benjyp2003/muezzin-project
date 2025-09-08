MAPPING = {
    "properties":
        {
            "file_name": {
                "type": "keyword"
            },
            "creation_data": {
                "type": "text"
            },
            "last_modified_date": {
                "type": "text"
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
            }
        }
}