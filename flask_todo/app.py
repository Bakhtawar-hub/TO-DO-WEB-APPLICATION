from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn = get_db()
        conn.execute('INSERT INTO todos (title, description) VALUES (?, ?)', (title, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE todos SET title = ?, description = ? WHERE id = ?', (title, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
