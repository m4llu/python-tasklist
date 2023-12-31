import tkinter as tk
import sqlite3

root = tk.Tk()
root.title("Login")
root.geometry("165x200")
root.resizable(width=False, height=False)
root.dashHeight = "325"

def dashboard():
    #this function is called when user logs in
    #creating window for the main dashboard
    global dash
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("290x"+root.dashHeight)
    dash.resizable(width=False, height=False)

    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tasks")

    sql = '''CREATE TABLE tasks (
        task VARCHAR(255)
    )'''

    c.execute(sql)
    conn.commit()
    conn.close()
    
    #layout
    task_label = tk.Label(dash, text="Tehtävä")
    task_label.grid(row=0, column=0, pady=(10,0))

    dashboard.task = tk.Entry(dash, width=30)
    dashboard.task.grid(row=0, column=1, padx=20, pady=(10,0))

    submit_btn = tk.Button(dash, text="Lisää tehtävä tietokantaan", width=25, command=lambda:[submit(), query()])
    submit_btn.grid(row=2, column=1, columnspan=2, pady=10, padx=20)

    query_btn = tk.Button(dash, text="Näytä tehtävät", width=25, command=query)
    query_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=20)

    select_label = tk.Label(dash, text="Valitse ID")
    select_label.grid(row=4, column=0, pady=5)

    dashboard.delete_box = tk.Entry(dash, width=30)   
    dashboard.delete_box.grid(row=5, column=1, pady=5)

    delete_btn = tk.Button(dash, text="Poista tehtävä", width=25, command=lambda:[delete(), query()])
    delete_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=20)

    edit_btn = tk.Button(dash, text="Muokkaa tehtävää", width=25, command=edit)
    edit_btn.grid(row=7, column=1, columnspan=2, pady=10, padx=20)


#query function
def query():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("SELECT task, oid FROM tasks")
    records = c.fetchall()
    print_records = " "

    for record in records:
        print_records += str(record[0]) + " \t " + str(record[1]) + "\n"

    heading_label = tk.Label(dash, text="Helvetica", font=("Helvetica", 16))
    heading_label['text'] = "Tehtävä \t ID"
    heading_label.grid(row=8, column=0, columnspan=2)

    # create query_label if it doesn't exist
    # update if exists
    if hasattr(dash, 'query_label'):
        dash.query_label['text'] = print_records
    else:
        dash.query_label = tk.Label(dash, text=print_records)
        dash.query_label.grid(row=9, column=0, columnspan=2)

    conn.commit()
    conn.close()
    
    
    #changes window height when task is added or deleted
def updateWindowHeight(increase):
    if increase == True:
        root.dashHeight = int(root.dashHeight) + 15
    else:
        root.dashHeight = int(root.dashHeight) - 15
    dash.geometry("290x"+str(root.dashHeight))
    
    
#submit task function
def submit():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    
    #check if entry is empty
    if dashboard.task.get() != "":
        c.execute("INSERT INTO tasks VALUES (:task)",
            {
                'task' : dashboard.task.get()
            })
        updateWindowHeight(True)
        
    conn.commit()
    conn.close()
    dashboard.task.delete(0, tk.END)
    
    
#delete task function
def delete():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE oid=" + dashboard.delete_box.get())
    dashboard.delete_box.delete(0, tk.END)
    conn.commit()
    conn.close()
    updateWindowHeight(False)


#update tasks function
def update():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    record_id = dashboard.delete_box.get()

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
    query()
    
    
#edit task function
def edit():
    #creating editor window
    global editor
    editor = tk.Tk()
    editor.title("Päivitä")
    editor.geometry("400x400")

    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    record_id = dashboard.delete_box.get()
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
   
    
#login function
def login():
    #getting the user inputs
    login.user = username.get()
    login.password = password.get()
    #this checks that password and username is correct
    if login.user == "admin" and login.password == "admin":
        dashboard()
        query()
        root.destroy()
    else:
        error_label.config(text="Virhe")

#root window layout
username_label = tk.Label(root, text="Käyttäjänimi")
username_label.grid(row=0, column=1, pady=(10,0))

username = tk.Entry(root, width=20)
username.grid(row=1, column=1, padx=20, pady=(10,0))

password_label = tk.Label(root, text="Salasana")
password_label.grid(row=2, column=1, pady=(10,0))

password = tk.Entry(root, width=20, show="*")
password.grid(row=3, column=1, padx=20, pady=(10,0))

login_btn = tk.Button(root, text="Kirjaudu", command=login)
login_btn.grid(row=4, column=1, columnspan=2, pady=10, padx=10)

error_label = tk.Label(root, text="")
error_label.grid(row=5, column=1, pady=(10,0))

root.mainloop()
