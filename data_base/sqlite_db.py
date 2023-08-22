import sqlite3 as sq

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect("friday_films.db")
    cur = base.cursor()
    if base:
        print("Data base connection ok")
    base.execute("CREATE TABLE IF NOT EXISTS films(film TEXT, status TEXT)")
    base.commit()


async def sql_add_film(film):
    cur.execute("INSERT INTO films VALUES (?, ?)", film)
    base.commit()


async def sql_change_status(film):
    cur.execute("UPDATE films SET status = 'watched' WHERE film = (?)", film)
    base.commit()


async def sql_show_suggestions(message, status):
    for film in cur.execute("SELECT film FROM films WHERE status = (?)", status):
        await bot.send_message(message.from_user.id, text=film[0])


async def sql_delete_film(film):
    cur.execute("DELETE FROM films WHERE film == ?", film)
    base.commit()
