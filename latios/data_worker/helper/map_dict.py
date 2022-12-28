import sqlite3

def map_dict(item: sqlite3.Row):
    return {
        key: item[key] for key in item.keys()
    }
