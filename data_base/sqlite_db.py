import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("friday_films.db")
    cur = base.cursor()
    if base:
        print("Data base connection ok")
    base.execute("CREATE TABLE IF NOT EXISTS films(film TEXT)")
    base.commit()


async def sql_add_film(film):
    cur.execute("INSERT INTO films VALUES (?)", tuple(film))
    base.commit()