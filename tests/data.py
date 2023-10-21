RESPONSE = {
    "batchcomplete": "",
    "continue": {"plcontinue": "29004|0|4th_Dimension_(Software)", "continue": "||"},
    "query": {
        "normalized": [
            {"from": "Land_assembly_district", "to": "Land assembly district"}
        ],
        "pages": {
            "123": {
                "pageid": 123,
                "ns": 0,
                "title": "Land assembly district",
                "links": [
                    {"ns": 0, "title": "Eminent domain"},
                    {"ns": 0, "title": "Holdout problem"},
                ],
            },
        },
    },
}

INPUT_GRAPH = {
    "a": ["b", "c", "d"],
    "b": ["a", "d", "e", "f"],
    "c": ["a", "f"],
    "d": ["a", "b"],
    "e": ["a", "g"],
    "f": ["b", "c", "d"],
    "g": ["a", "d", "e"],
}
