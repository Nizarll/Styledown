from flask import render_template
from app import app, socketio
from app.parser import Parser
from app.generator import Generator

import time
import os
import threading

def parse_file(file):
    parser = Parser(file)
    tokens = parser.parse()
    generator = Generator(tokens, parser.links)
    html_output = generator.generate_html()
    print(parser.links)
    return html_output

def render_template_outside_app(file):
    with app.app_context():
        html_content = render_template('view.html', content=parse_file(file))
        return html_content

@app.route("/")
def home():
    
    html_output = parse_file(markdown_file)
    return render_template("view.html", content=html_output, file_name="test")

def start_server(file_name):
    """Démarrer le serveur Flask et surveiller les modifications."""
    global markdown_file
    markdown_file = file_name
    threading.Thread(target=watch_file, args=(file_name,), daemon=True).start()
    socketio.run(app, debug=True)

def watch_file(file_name):
    last_modified = 0
    try:
        stat = os.stat(file_name)
        last_modified = stat.st_mtime
    except FileNotFoundError:
        return
    except PermissionError:
        return
    while True:
        time.sleep(.1)
        try:
            stat = os.stat(file_name)
            current_modified = stat.st_mtime
            if current_modified != last_modified:
                last_modified = current_modified
                updated_html = render_template_outside_app(markdown_file)
                socketio.emit("update", {'html': updated_html})
        except FileNotFoundError:
            break
        except PermissionError:
            break

#@socketio.on()
