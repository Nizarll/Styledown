import os

MARKDOWN_DIRECTORY = "markdowns"



def create_markdown(file_name):
    """Créer un nouveau fichier Markdown."""
    if not file_name.endswith(".md"):
        file_name += ".md"
    file_path = os.path.join(MARKDOWN_DIRECTORY, file_name)
    if os.path.exists(file_path):
        print(f"Le fichier '{file_name}' existe déjà.")
        return
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Nouveau fichier Markdown\n\nCommencez à écrire ici...\n")
    print(f"Fichier '{file_name}' créé avec succès.")

def delete_markdown(file_name):
    """Supprimer un fichier Markdown."""
    file_path = os.path.join(MARKDOWN_DIRECTORY, file_name)
    if not os.path.exists(file_path):
        print(f"Le fichier '{file_name}' n'existe pas.")
        return
    os.remove(file_path)
    print(f"Fichier '{file_name}' supprimé avec succès.")

def list_markdown_files():
    """Lister les fichiers Markdown."""
    files = [f for f in os.listdir(MARKDOWN_DIRECTORY) if f.endswith(".md")]
    if not files:
        print("Aucun fichier Markdown trouvé.")
    else:
        print("Fichiers Markdown disponibles :")
        for file in files:
            print(f"- {file}")
