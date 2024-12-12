import os
import sys
import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import re

app = Flask(__name__)
socketio = SocketIO(app)

markdown_file = ""

@app.route("/")
def home():
    """Route principale pour afficher le Markdown converti en HTML."""
    if not os.path.exists(markdown_file):
        return f"<h1>Erreur : le fichier '{markdown_file}' n'existe pas !</h1>"
    
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    html_content = parse_custom_markdown(markdown_content)

    file_name = os.path.splitext(os.path.basename(markdown_file))[0]

    return render_template("preview.html", content=html_content, file_name=file_name)

def parse_custom_markdown(markdown_text):
    """Convertir le Markdown personnalisé en HTML stylisé avec des classes Tailwind."""

    markdown_text = re.sub(
        r"\[size=(.+?) color=(.+?)\](.+?)\[/size\]",
        r'<span style="font-size:\1; color:\2;">\3</span>',
        markdown_text,
    )

    markdown_text = re.sub(
        r"\[block type=(.+?)\](.+?)\[/block\]",
        r'<div class="block-\1 p-4 rounded-lg bg-\1-100 text-\1-800 border-l-4 border-\1-400 shadow-sm">\2</div>',
        markdown_text,
        flags=re.DOTALL,
    )

    markdown_text = re.sub(
        r"\[button color=(.+?) link=(.+?)\](.+?)\[/button\]",
        r'<a href="\2" class="bg-\1-500 text-white py-2 px-4 rounded hover:bg-\1-600 inline-block mt-4">\3</a>',
        markdown_text,
    )

    markdown_text = re.sub(r"^### (.+)$", r'<h3 class="text-xl font-semibold mt-4">\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^## (.+)$", r'<h2 class="text-2xl font-bold mt-6">\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^# (.+)$", r'<h1 class="text-3xl font-extrabold mt-8">\1</h1>', markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(
        r"^> (.+)$",
        r'<blockquote class="border-l-4 pl-4 italic text-gray-600 border-gray-300">\1</blockquote>',
        markdown_text,
        flags=re.MULTILINE,
    )

    markdown_text = re.sub(r"^- (.+)$", r'<li class="mb-1">\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"(<li.*?</li>)", r'<ul class="list-disc pl-8">\1</ul>', markdown_text, flags=re.DOTALL)

    markdown_text = re.sub(r"^\d+\. (.+)$", r'<li class="mb-1">\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"(<li.*?</li>)", r'<ol class="list-decimal pl-8">\1</ol>', markdown_text, flags=re.DOTALL)

    markdown_text = re.sub(
    r"```(\w+)?\n(.*?)```",  
    r'<pre class="rounded-lg bg-gray-100 p-4 overflow-x-auto"><code class="language-\1">\2</code></pre>',
    markdown_text,
    flags=re.DOTALL,
)

    return markdown_text



def create_markdown(file_name):
    """Créer un nouveau fichier Markdown."""
    if not file_name.endswith(".md"):
        file_name += ".md"
    
    if os.path.exists(file_name):
        print(f"Le fichier '{file_name}' existe déjà.")
        return
    
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("# Nouveau fichier Markdown\n\nCommencez à écrire ici...\n")
    
    print(f"Fichier '{file_name}' créé avec succès.")

def delete_markdown(file_name):
    """Supprimer un fichier Markdown."""
    if not os.path.exists(file_name):
        print(f"Le fichier '{file_name}' n'existe pas.")
        return
    
    os.remove(file_name)
    print(f"Fichier '{file_name}' supprimé avec succès.")

def open_editor(file_name):
    """Ouvrir le fichier dans l'éditeur par défaut."""
    try:
        if os.name == "nt":  
            os.startfile(file_name)
        elif os.name == "posix":  
            subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", file_name])
    except Exception as e:
        print(f"Impossible d'ouvrir le fichier : {e}")

def start_server(file_name):
    """Démarrer le serveur Flask et surveiller les modifications."""
    global markdown_file
    markdown_file = file_name

    threading.Thread(target=watch_file, args=(file_name,), daemon=True).start()

    socketio.run(app, debug=True)

def watch_file(file_name):
    """Surveiller les modifications du fichier."""
    last_modified = os.path.getmtime(file_name)
    while True:
        try:
            current_modified = os.path.getmtime(file_name)
            if current_modified != last_modified:
                last_modified = current_modified
                socketio.emit('update')  
        except FileNotFoundError:
            break

def list_markdown_files():
    """Lister tous les fichiers Markdown dans le répertoire courant."""
    files = [f for f in os.listdir('.') if f.endswith('.md')]
    if not files:
        print("Aucun fichier Markdown trouvé dans le répertoire courant.")
    else:
        print("Fichiers Markdown disponibles :")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

def main():
    """Point d'entrée du CLI."""
    if len(sys.argv) < 2:
        print("Usage :")
        print("  python mymd.py create <nom-du-fichier>")
        print("  python mymd.py delete <nom-du-fichier>")
        print("  python mymd.py preview <nom-du-fichier>")
        print("  python mymd.py list")
        return
    
    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Veuillez fournir un nom de fichier.")
        else:
            create_markdown(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Veuillez fournir un nom de fichier.")
        else:
            delete_markdown(sys.argv[2])
    elif command == "preview":
        if len(sys.argv) < 3:
            print("Veuillez fournir un nom de fichier.")
        else:
            file_name = sys.argv[2]
            if not os.path.exists(file_name):
                print(f"Le fichier '{file_name}' n'existe pas.")
            else:
                open_editor(file_name)  
                start_server(file_name)  
    elif command == "list":
        list_markdown_files()  
    else:
        print(f"Commande inconnue : '{command}'.")
        print("Commandes disponibles : create, delete, preview, list")


if __name__ == "__main__":
    main()
