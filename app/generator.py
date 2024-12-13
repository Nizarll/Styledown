from app.parser import Parser
from app.markdown import MdTag, MdKind, MdHeading, MdTask, MdList, MdQuote, TaskKind
from app.svgs import *

import html
import os

class Generator:
    def __init__(self, tokens):
        self.tokens = tokens

    def generate_html(self):

        html_output = [
            '<!DOCTYPE html>',
            '<html>',
            '<script src"https://cdn.jsdelivr.net/npm/windicss@3.5.6/index.min.js"></script>'
                '<head><title>Markdown</title></head>',
            '<body class="dark">',
        ]

        for token in self.tokens:
            if token.kind == MdKind.HEADING:
                html_output.append(self._generate_heading(token.heading))
            elif token.kind == MdKind.TASK:
                html_output.append(self._generate_task(token.task))
            elif token.kind == MdKind.LIST:
                html_output.append(self._generate_list(token.list))
            elif token.kind == MdKind.QUOTE:
                html_output.append(self._generate_quote(token.quote))

        html_output.append("</body>")
        html_output.append("</html>")

        return "\n".join(html_output)

    def _generate_heading(self, heading: MdHeading):
        content = heading.content
        return f"<h{heading.level}>{html.escape(content)}</h{heading.level}>"

    def _generate_task(self, task: MdTask):
        checked = "checked" if task.kind == TaskKind.CHECKBOX_FILLED else ""
        description = task.description
        if task.kind == TaskKind.CHECKBOX_FILLED or task.kind == TaskKind.CHECKBOX_EMPTY:
            return f'<div><input type="checkbox" {checked} disabled> {html.escape(description)}</div>'
        elif task.kind == TaskKind.WARNING:

            return f'<div class="bg-amber-100 dark:bg-amber-200/60 border-l-4 border-yellow-500 py-1 px-4" ><div class="flex flex-row py-1 w-full text-amber-800 dark:text-amber-100 font-bold ">{warning_icon('text-amber-800 dark:text-amber-100')} <div class="py-2 px-2">Caution</div></div>{html.escape(description)}</div>'
        elif task.kind == TaskKind.EMERGENCY:
            return f'<div class="dark:bg-red-200/60 bg-red-50 border-l-4 border-red-500 py-1 px-4" ><div class="flex flex-row py-1 w-full text-red-800 dark:text-red-300 font-bold">{emergency_icon('text-red-800 dark:text-red-300')} <div class="py-2 px-2">Emergency</div></div>{html.escape(description)}</div>'


    def _generate_list(self, md_list: MdList):
        list_items = [f"<li>{html.escape(item)}</li>" for item in md_list.items]
        return "<ul>" + "\n".join(list_items) + "</ul>"

    def _generate_quote(self, quote: MdQuote):
        content = quote.content
        return f'<blockquote>{html.escape(content)}</blockquote>'

