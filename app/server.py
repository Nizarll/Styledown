from flask import render_template
from app import app, socketio
from app.parser import Parser
from app.generator import Generator
from app.utils import Env

import time
import os
import threading

MARKDOWN_DIRECTORY = "markdowns"
markdown_file = ""

FILE = 'markdowns/test'

def parse_file(file):
    parser = Parser(file, Env(files=None))
    tokens = parser.parse()
    generator = Generator(tokens)
    html_output = generator.generate_html()
    return html_output

def render_template_outside_app(file):
    with app.app_context():
        html_content = render_template('preview.html', content=parse_file(file))
        return html_content

@app.route("/")
def home():
    
    # file_path = os.path.join(MARKDOWN_DIRECTORY, markdown_file)
    # if not os.path.exists(file_path):
    #     return f"<h1>Erreur : le fichier '{markdown_file}' n'existe pas.</h1>"
    # 
    # with open(file_path, "r", encoding="utf-8") as f:
    #     markdown_content = f.read()
    #html_content = parse_custom_markdown(markdown_content)
    #with open("output.html", "w") as f:
    #    f.write(html_output)
    
    html_output = parse_file(FILE)
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
        time.sleep(.1)
        try:
            stat = os.stat(file_path)
            current_modified = stat.st_mtime
            if current_modified != last_modified:
                last_modified = current_modified
                updated_html = render_template_outside_app(FILE)
                socketio.emit("update", {'html': updated_html})
        except FileNotFoundError:
            break
        except PermissionError:
            break
