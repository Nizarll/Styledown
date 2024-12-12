import re

def parse_custom_markdown(markdown_text):
    """Convertir le Markdown personnalisé en HTML stylisé."""
    # Balises personnalisées
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

    '''Syntaxe Markdown calssique'''

    # Titres
    markdown_text = re.sub(r"^### (.+)$", r'<h3 class="text-xl font-semibold mt-4">\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^## (.+)$", r'<h2 class="text-2xl font-bold mt-6">\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^# (.+)$", r'<h1 class="text-3xl font-extrabold mt-8">\1</h1>', markdown_text, flags=re.MULTILINE)

    # Gras
    markdown_text = re.sub(r"\*\*(.+?)\*\*",r"<strong>\1</strong>", markdown_text)

    # Italique
    markdown_text = re.sub(r"\*(.+?)\*",r"<strong><em>\1</em></strong>", markdown_text)

    # Gars et Italique
    markdown_text = re.sub(r"\*\*\*(.+?)\*\*\*",r"<strong><em>\1</em></strong>", markdown_text)

    # Texte Barre
    markdown_text = re.sub(r"~~(.+?)~~",r"<del>\1</del>", markdown_text)

    #Retour a la ligne
    markdown_text = re.sub(r"\\",r"<br />",markdown_text)

    #Images
    markdown_text = re.sub(
        r"!\[(.*?)\]\((.*?)\)", 
        r'<img src="\2" alt="\1" class="my-4 max-w-full h-auto mx-auto">',
        markdown_text
    )

    #Alignement
    markdown_text = re.sub(
        r"\[align=(left|center|right)\](.+?)\[/align\]",
        r'<div style="text-align:\1;">\2</div>',
        markdown_text,
        flags=re.DOTALL
    )

    #Icones
    markdown_text = re.sub(
        r"\[icon=(.+?)\]",
        r'<i class="fa fa-\1"></i>',
        markdown_text
    )

    # Citations
    markdown_text = re.sub(
        r"^> (.+)$",
        r'<blockquote class="border-l-4 pl-4 italic text-gray-600 border-gray-300">\1</blockquote>',
        markdown_text,
        flags=re.MULTILINE,
    )

    # Listes
    markdown_text = re.sub(r"^- (.+)$", r'<li class="mb-1">\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"(<li.*?</li>)", r'<ul class="list-disc pl-8">\1</ul>', markdown_text, flags=re.DOTALL)

    # Blocs de code
    markdown_text = re.sub(
        r"```(\w+)?\n(.*?)```",
        r'<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code class="language-\1">\2</code></pre>',
        markdown_text,
        flags=re.DOTALL,
    )

    #Tableaux
    markdown_text = re.sub(
        r"^\|(.+?)\|\n\|([-:| ]+)\|\n((?:\|.*?\|\n)*)",
        lambda match: generate_table_html(match.group(1), match.group(2), match.group(3)),
        markdown_text,
        flags=re.MULTILINE
    )

    return markdown_text

def generate_table_html(headers, alignments, rows):
    # Gérer les en-têtes
    headers_html = "".join([f"<th>{header.strip()}</th>" for header in headers.split("|")])
    
    # Gérer les alignements
    alignments = alignments.split("|")
    alignment_styles = [
        "text-left" if ":" in align and align.endswith(":") else
        "text-right" if ":" in align and align.startswith(":") else
        "text-center" if ":" in align else "text-left"
        for align in alignments
    ]
    
    # Gérer les lignes
    rows_html = ""
    for row in rows.strip().split("\n"):
        row_html = "".join([f"<td>{col.strip()}</td>" for col in row.split("|")])
        rows_html += f"<tr>{row_html}</tr>"
    
    return f"<table class='table-auto border-collapse border border-gray-300'><thead><tr>{headers_html}</tr></thead><tbody>{rows_html}</tbody></table>"