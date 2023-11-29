import tkinter as tk
import sqlite3

root = tk.Tk()
root.title("Tietokanta")
root.geometry("400x400")

def dashboard():
    global dash
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("400x400")

    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tasks")

    sql = '''CREATE TABLE tasks (
        task VARCHAR(255)
    )'''

    c.execute(sql)
    conn.commit()
    conn.close()

    task_label = tk.Label(dash, text="Tehtävä")
    task_label.grid(row=0, column=0, pady=(10,0))

    task = tk.Entry(dash, width=30)
    task.grid(row=0, column=1, padx=20, pady=(10,0))

    submit_btn = tk.Button(dash, text="Lisää tehtävä tietokantaan", command=submit)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    query_btn = tk.Button(dash, text="Näytä tehtävät", command=query)
    query_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    select_label = tk.Label(dash, text="Valitse ID")
    select_label.grid(row=4, column=0, pady=5)

    delete_box = tk.Entry(dash, width=30)
    delete_box.grid(row=5, column=1, pady=5)

    delete_btn = tk.Button(dash, text="Poista tehtävä", command=delete)
    delete_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    edit_btn = tk.Button(dash, text="Muokkaa tehtävää", command=edit)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10)


query_label = tk.Label(root)


def query():
    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    c.execute("SELECT task, oid FROM tasks")
    records = c.fetchall()
    print_records = " "

    for record in records:
        print_records += str(record[0]) + " \t " + str(record[1]) + "\n"

    heading_label = tk.Label(root, text="Helvetica", font=("Helvetica", 16))

    heading_label['text'] = "Tehtävä \t ID"
    heading_label.grid(row=8, column=0, columnspan=2)

    query_label['text'] = print_records
    query_label.grid(row=9, column=0, columnspan=2)

    conn.commit()
    conn.close()

def submit():
    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    c.execute("INSERT INTO tasks VALUES (:task)",
        {
            'task' : task.get()
        })
    
    conn.commit()
    conn.close()
    task.delete(0, tk.END)

def delete():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE oid=" + delete_box.get())

    delete_box.delete(0, tk.END)

    conn.commit()
    conn.close()


def update():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    record_id = delete_box.get()

    c.execute("""UPDATE tasks SET
        task = :task
              
        WHERE oid = :oid""",
        {
            'task': task_editor.get(),
            'oid': record_id
        })

    conn.commit()
    conn.close()
    editor.destroy()

def edit():
    global editor
    editor = tk.Tk()
    editor.title("Päivitä")
    editor.geometry("400x400")

    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM tasks WHERE oid = " + record_id)
    records=c.fetchall()

    global task_editor

    task_label = tk.Label(editor, text="Tehtävä")
    task_label.grid(row=0, column=0, pady=(10,0))

    task_editor = tk.Entry(editor, width=30)
    task_editor.grid(row=0, column=1, padx=20, pady=(10,0))

    for record in records:
        task_editor.insert(0, record[0])

    save_btn = tk.Button(editor, text="Tallenna", command=update)
    save_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    

def login():
    pass

username_label = tk.Label(root, text="Käyttäjänimi")
username_label.grid(row=0, column=1, pady=(10,0))

username = tk.Entry(root, width=30)
username.grid(row=1, column=1, padx=20, pady=(10,0))

password_label = tk.Label(root, text="Salasana")
password_label.grid(row=2, column=1, pady=(10,0))

password = tk.Entry(root, width=30, show="*")
password.grid(row=3, column=1, padx=20, pady=(10,0))

login_btn = tk.Button(root, text="Kirjaudu", command=login)
login_btn.grid(row=4, column=1, columnspan=2, pady=10, padx=10)

root.mainloop()
