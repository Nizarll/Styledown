from flask import render_template
from app import app, socketio
#from app.markdowns import parse_custom_markdown
from app.parser import Parser
from app.generator import Generator

import time
import os
import threading

MARKDOWN_DIRECTORY = "markdowns"
markdown_file = ""

@app.route("/")
def home():
    """Afficher le fichier Markdown converti."""
    # file_path = os.path.join(MARKDOWN_DIRECTORY, markdown_file)
    # if not os.path.exists(file_path):
    #     return f"<h1>Erreur : le fichier '{markdown_file}' n'existe pas.</h1>"
    # 
    # with open(file_path, "r", encoding="utf-8") as f:
    #     markdown_content = f.read()
    #html_content = parse_custom_markdown(markdown_content)
    parser = Parser('markdowns/test')
    tokens = parser.parse()
    generator = Generator(tokens)
    html_output = generator.generate_html()
    #with open("output.html", "w") as f:
    #    f.write(html_output)

    return render_template("preview.html", content=html_output, file_name="test")

def start_server(file_name):
    """Démarrer le serveur Flask et surveiller les modifications."""
    global markdown_file
    markdown_file = file_name

    threading.Thread(target=watch_file, args=(file_name,), daemon=True).start()

    socketio.run(app, debug=True)

def watch_file(file_name):
    file_path = os.path.join(MARKDOWN_DIRECTORY, file_name)
    last_modified = 0
    try:
        stat = os.stat(file_path)
        last_modified = stat.st_mtime
    except FileNotFoundError:
        return
    except PermissionError:
        return
    while True:
        try:
            stat = os.stat(file_path)
            current_modified = stat.st_mtime
            if current_modified != last_modified:
                last_modified = current_modified
                socketio.emit("update")
        except FileNotFoundError:
            break
        except PermissionError:
            break
        time.sleep(.05)
