import sqlite3,random
conn = sqlite3.connect('db1.db', check_same_thread=False)
cursor = conn.cursor()
def add_user(user_id: int, username: str, name: str, last_name: str):
	cursor.execute('INSERT INTO users (user_id, username, name, last_name) VALUES (?, ?, ?, ?)', (user_id, username, name, last_name))
	conn.commit()
def add_admin(user_id: int):
        cursor.execute('INSERT INTO admins (user_id) VALUES (?)', (user_id,))
        conn.commit()  
def remove_admin(user_id1):
        cursor.execute(f"DELETE FROM admins WHERE user_id={user_id1}")
        conn.commit()
def droch(user_id1, drochk):
        cursor.execute('INSERT OR REPLACE INTO droch(user_id, drochka) VALUES(?,?)', [f'{user_id1}',f'{drochk}'])
        conn.commit()
def get_droch(user_id1):
        cursor.execute(f'SELECT drochka FROM droch WHERE user_id={user_id1}')
        jon = cursor.fetchone()
        if jon == None:
                return jon
        else:
                return jon[0]
def items(user_id1, drolin1):
        cursor.execute('INSERT OR REPLACE INTO items(user_id, drolin) VALUES(?,?)', [f'{user_id1}',f'{drolin1}'])
        conn.commit()
def items_ex_capt(user_id1, ex_capt1):
    cursor.execute('INSERT OR REPLACE INTO items_capt(user_id, ex_capt) VALUES(?,?)', [f'{user_id1}', f'{ex_capt1}'])
    conn.commit()
def get_lin(user_id1):
        cursor.execute(f'SELECT drolin FROM items WHERE user_id={user_id1}')
        jon = cursor.fetchone()
        if jon == None:
                return jon
        else:
                return jon[0]
def get_excapt(user_id1):
        cursor.execute(f'SELECT ex_capt FROM items_capt WHERE user_id={user_id1}')
        jon = cursor.fetchone()
        if jon == None:
                return jon
        else:
                return jon[0]        
def towns(user_id1, town):
        cursor.execute('INSERT OR REPLACE INTO capt(user_id, towns) VALUES(?,?)', [f'{user_id1}',f'{town}'])
        conn.commit()
def get_towns(user_id1):
        cursor.execute(f'SELECT towns FROM capt WHERE user_id={user_id1}')
        jon = cursor.fetchone()
        if jon == None:
                return jon
        else:
                return jon[0]


def get_admin():
        admins = []
        cursor.execute('SELECT * FROM admins;')
        jon = cursor.fetchall()
        for i in jon:
                admins.append(i[0])
        return admins
def get_capt_top():
        top_u=[]
        top_c=[]
        a=0
        cursor.execute('SELECT * FROM capt')
        jon = cursor.fetchall()
        jon.sort()
        jon.reverse()
        while a != 3:
                cursor.execute(f'SELECT user_id FROM capt WHERE towns={jon[0][0]}')
                top_u.append(jon[0][1])
                top_c.append(jon[0][0])
                jon.remove(jon[0])
                a+=1
        a=0
        b=1
        text=''
        for i in top_u:
                text=text+f'<a href="tg://user?id={i}">Топ {b}</a>(кликабельно) Всего {top_c[a]} захватов '
                text=text+'\n'
                a+=1
                b+=1
        return text

                

def get_win():
        winners=[]
        for i in range(5):
                cursor.execute(f'SELECT numb, name FROM part WHERE name ={random.randint(1,20)}')
                jon = cursor.fetchone()
                if not jon[0] in winners:
                        winners.append(jon[0])
                else:
                        cursor.execute(f'SELECT numb, name FROM part WHERE name ={random.randint(1,20)}')
                        jon = cursor.fetchone()
                        winners.append(jon[0])
        return winners
def money(user_id1, money):
        cursor.execute('INSERT OR REPLACE INTO money(user_id, money) VALUES(?,?)', [f'{user_id1}',f'{money}'])
        conn.commit()
def get_money(user_id1):
        cursor.execute(f'SELECT money FROM money WHERE user_id={user_id1}')
        jon = cursor.fetchone()
        if jon == None:
                return jon
        else:
                return jon[0]
