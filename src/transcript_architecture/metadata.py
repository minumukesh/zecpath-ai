METADATA_STANDARDS = {

    "candidate_id": {

        "type": "string",

        "required": True,

        "description":
            "Unique identifier of the candidate.",
    },


    "job_id": {

        "type": "string",

        "required": True,

        "description":
            "Unique identifier of the job.",
    },


    "question_id": {

        "type": "string",

        "required": True,

        "description":
            "Unique identifier of the screening question.",
    },


    "timestamp": {

        "type": "ISO-8601 datetime",

        "required": True,

        "description":
            "Time at which the transcript interaction was recorded.",
    },


    "confidence_level": {

        "type": "float",

        "range": "0.0-1.0",

        "required": True,

        "description":
            "Speech-to-text confidence level for the transcript segment.",
    },


    "speaker": {

        "type": "enum",

        "values": [
            "candidate",
            "interviewer",
            "system",
        ],

        "required": True,

        "description":
            "Source of the transcript segment.",
    },


    "sequence": {

        "type": "integer",

        "required": True,

        "description":
            "Order of the transcript segment in the conversation.",
    },


    "text": {

        "type": "string",

        "required": True,

        "description":
            "Normalized transcript text.",
    },


    "language": {

        "type": "string",

        "required": True,

        "description":
            "Language of the transcript segment.",
    },
}
