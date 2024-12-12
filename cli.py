import sys
from app.server import start_server
from app.parser import create_markdown, delete_markdown, list_markdown_files

def main():
    """CLI pour gérer les commandes Markdown."""
    if len(sys.argv) < 2:
        print("Usage :")
        print("  python cli.py create <nom-du-fichier>")
        print("  python cli.py delete <nom-du-fichier>")
        print("  python cli.py list")
        print("  python cli.py preview <nom-du-fichier>")
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
    elif command == "list":
        list_markdown_files()
    elif command == "preview":
        if len(sys.argv) < 3:
            print("Veuillez fournir un nom de fichier.")
        else:
            start_server(sys.argv[2])
    else:
        print(f"Commande inconnue : '{command}'.")

if __name__ == "__main__":
    main()
