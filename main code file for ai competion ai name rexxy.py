import tkinter as tk
import sqlite3
import pyttsx3
import math
from typing import Callable, Dict, Any
import wikipedia
import os
from duckduckgo_search import DDGS




engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

conn = sqlite3.connect("REXXY_memory.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
question TEXT PRIMARY KEY,
answer TEXT
)
""")


cursor.execute("PRAGMA table_info(memory)")
cols = [c[1] for c in cursor.fetchall()]

if "answer" not in cols:
    cursor.execute("DROP TABLE memory")
    cursor.execute("""
    CREATE TABLE memory(
    question TEXT PRIMARY KEY,
    answer TEXT
    )
    """)


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT,
password TEXT
)
""")

conn.commit()


def remember(q,a):
    cursor.execute(
    "INSERT OR REPLACE INTO memory(question,answer) VALUES (?,?)",
    (q,a)
    )
    conn.commit()

def recall(q):
    cursor.execute(
    "SELECT answer FROM memory WHERE question=?",
    (q,)
    )
    data = cursor.fetchone()

    if data:
        return data[0]

    return None

def search_web(query):

    text=""

    with DDGS() as ddgs:

        results = ddgs.text(query,max_results=3)

        for r in results:

            text += r["body"]+"\n"

            print("LINK:",r["href"])

    return text[:500]


def brain(cmd):
    cmd = cmd.lower()

    
    memory = recall(cmd)

    if memory:
        return memory

    
    if "who created you" in cmd:
        return "My creator is Aashish tripath team unwanted ."

    
    if "taj mahal" in cmd:

        ans = wikipedia.summary("Taj Mahal",2)

        remember(cmd,ans)

        return ans

    if "open notepad" in cmd:

        speak("Opening notepad")

        os.system("notepad")

        return "Notepad opened"

    if "open chrome" in cmd:

        speak("Opening chrome")

        os.system("start chrome")

        return "Chrome opened"

    if "open vs code" in cmd:

        speak("Opening VS Code")

        os.system("code")

        return "VS Code opened"

    if "shutdown computer" in cmd:

        os.system("shutdown /s /t 10")

        return "Shutting down computer"
    if "open blender" in cmd:

        speak ("opening blender")
        os.system("blender")
        return "blender opened"
    if "open pycharm" in cmd: 

        speak("opening pycharm")
        os.system("pycharm")
        return "pycharm opened"
    if "open ms word"in cmd:  
        speak("opening ms word")
        os.system("ms word")
        return "ms word opened"
    if "open ms excel" in cmd:
        speak ("opening ms excel")
        os.system("ms excel")
        return "ms excel opened"
    if " open ms powerpoint " in cmd:
        speak ("opening ms powerpoint")
        os.system("ms powerpoint")
        return "ms powerpoint opened"
    if "open calculator" in cmd:
        speak ("opening calculator ")
        os.system("calc")
        return "calculator opened"
    if "open paint" in cmd:
        speak ("opening paint")
        os . system("mspaint")
        return "paint opened "
    if "open command prompt" in cmd:
        speak ("opening command prompt")
        os.system("cmd")
        return " command prompt opened"
    if "open control panel"in cmd:
        speak ("opening control panel")
        os.system("control")
        return "control panel opened"
    if "open task manager" in cmd:
        speak ("opening task manager")
        os.system("taskmgr")
        return "task manager opened"
    if "open device manager" in cmd:
      speak ("opening device manager")
      os.system("devmgmt.msc")
      return "device manager opened"
    if "open registry editor" in cmd:
        speak ("opening registry editor")
        os.system("regedit")
        return "registry editor opened"
    if "open system configuration" in cmd:
        speak ("opening system configuration")
        os.system("msconfig")
        return "system configuration opened"
    if "open event viewer" in cmd:
        speak ("opening event viewer")
        os.system("eventvwr.msc")
        return "event viewer opened"
    if "open disk management" in cmd:
        speak ("opening disk management")
        os.system("diskmgmt.msc")
        return "disk management opened"       
    if "open services" in cmd:
        speak ("opening services")
        os.system("services.msc")
        return "services opened"
        
    if any(word in cmd for word in ["calculate", "+", "-", "*", "/", "add", "subtract", "multiply", "divide"]):
        try:
            
            calc_cmd = cmd.replace("calculate", "")
            calc_cmd = calc_cmd.replace("add", "+").replace("plus", "+")
            calc_cmd = calc_cmd.replace("subtract", "-").replace("minus", "-")
            calc_cmd = calc_cmd.replace("multiply", "*").replace("times", "*")
            calc_cmd = calc_cmd.replace("divide", "/").replace("divided by", "/")
            
            
            filtered_chars = "".join(c for c in calc_cmd if c in "0123456789+-*/.() ")
            
            
            if filtered_chars.strip():
                result = eval(filtered_chars)
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                ans = f"The answer is {result}"
                remember(cmd, ans)
                return ans
        except ZeroDivisionError:
            return "You cannot divide by zero."
        except Exception:
            return "Sorry, I couldn't calculate that. Please try a simpler format like: 5 + 5"

    
    try:

        ans = wikipedia.summary(cmd,2)

        remember(cmd,ans)

        return ans

    except:
        pass

    
    ans = search_web(cmd)

    if ans:

        remember(cmd,ans)

        return ans

    return "I do not know yet but I will learn."


root = tk.Tk()
root.title("REXXY AI")
root.geometry("600x600")
root.configure(bg="black")


canvas = tk.Canvas(root,width=200,height=200,bg="black",highlightthickness=0)
canvas.pack(pady=10)

angle = 0

def animate():

    global angle

    canvas.delete("all")

    canvas.create_arc(
    20,20,180,180,
    start=angle,
    extent=120,
    style="arc",
    outline="cyan",
    width=4
    )

    angle = (angle + 5) % 360

    root.after(50, animate)

animate()


chat = tk.Text(root,height=18,width=70,bg="black",fg="cyan")
chat.pack()

entry = tk.Entry(root,width=50)
entry.pack(pady=10)

def send():

    cmd = entry.get()

    if cmd.strip()=="":
        return

    chat.insert(tk.END,"\nYOU: "+cmd+"\n")

    res = brain(cmd)

    chat.insert(tk.END,"AI: "+res+"\n")

    speak(res)

    entry.delete(0,tk.END)

btn = tk.Button(root,text="SEND",command=send)
btn.pack()


def login():

    win = tk.Toplevel()
    win.title("Login")

    tk.Label(win,text="Username").pack()

    u = tk.Entry(win)
    u.pack()

    tk.Label(win,text="Password").pack()

    p = tk.Entry(win,show="*")
    p.pack()

    def check():

        cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (u.get(),p.get())
        )

        if cursor.fetchone():

            speak("Login successful")

            win.destroy()

        else:

            speak("Wrong login")

    tk.Button(win,text="Login",command=check).pack()

def register():

    win = tk.Toplevel()
    win.title("Create Account")

    tk.Label(win,text="Username").pack()

    u = tk.Entry(win)
    u.pack()

    tk.Label(win,text="Password").pack()

    p = tk.Entry(win,show="*")
    p.pack()

    def create():

        cursor.execute(
        "INSERT INTO users VALUES (?,?)",
        (u.get(),p.get())
        )

        conn.commit()

        speak("Account created")

        win.destroy()

    tk.Button(win,text="Create",command=create).pack()


menu = tk.Menu(root)
root.config(menu=menu)

account = tk.Menu(menu)

menu.add_cascade(label="Account",menu=account)

account.add_command(label="Login",command=login)
account.add_command(label="Create Account",command=register)


speak("REXXY AI ready")

root.mainloop()
