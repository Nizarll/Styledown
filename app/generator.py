from app.parser import Parser
from app.markdown import MdTag, MdKind, MdHeading, MdTask, MdList, MdQuote, MdCode, TaskKind
from app.svgs import *

import html
import os

class Generator:
    def __init__(self, tokens):
        self.tokens = tokens

    def generate_html(self):

        html_output = [ ]

        for token in self.tokens:
            if token.kind == MdKind.HEADING:
                html_output.append(self._generate_heading(token.heading))
            elif token.kind == MdKind.TASK:
                html_output.append(self._generate_task(token.task))
            elif token.kind == MdKind.LIST:
                html_output.append(self._generate_list(token.list))
            elif token.kind == MdKind.QUOTE:
                html_output.append(self._generate_quote(token.quote))
            elif token.kind == MdKind.CODE:
                html_output.append(self._generate_code(token.code))

        html_output.append("</body>")
        html_output.append("</html>")

        return "\n".join(html_output)

    def _generate_heading(self, heading: MdHeading):
        content = heading.content
        return f"<h{heading.level} class='text-{heading.level * 2}xl font-bold mb-4'>{html.escape(content)}</h{heading.level}>"

    def _generate_task(self, task: MdTask):
        checked = "checked" if task.kind == TaskKind.CHECKBOX_FILLED else ""
        description = task.description
        if task.kind == TaskKind.CHECKBOX_FILLED or task.kind == TaskKind.CHECKBOX_EMPTY:
            return f'<div class="flex items-center mb-2"><input type="checkbox" {checked} disabled class="mr-2"> <span>{html.escape(description)}</span></div>'
        elif task.kind == TaskKind.WARNING:
            return f'<div class="bg-amber-100 dark:bg-amber-200/60 border-l-4 border-yellow-500 py-2 px-4 mb-4"><div class="flex items-center text-amber-800 dark:text-amber-100 font-bold">{warning_icon("text-amber-800 dark:text-amber-100")}<span class="ml-2">Caution</span></div><p>{html.escape(description)}</p></div>'
        elif task.kind == TaskKind.EMERGENCY:
            return f'<div class="dark:bg-red-200/60 bg-red-50 border-l-4 border-red-500 py-2 px-4 mb-4"><div class="flex items-center text-red-800 dark:text-red-300 font-bold">{emergency_icon("text-red-800 dark:text-red-300")}<span class="ml-2">Emergency</span></div><p>{html.escape(description)}</p></div>'

    def _generate_list(self, md_list: MdList):
        list_items = [f"<li class='mb-1'>{html.escape(item)}</li>" for item in md_list.items]
        return "<ul class='list-disc pl-5 mb-4'>" + "\n".join(list_items) + "</ul>"

    def _generate_quote(self, quote: MdQuote):
        content = quote.content
        return f"<div class='border-l-4 border-gray-600 pl-4 italic'>{html.escape(content)}</div>"

    def _generate_code(self, code: MdCode):
        content = code.content
        language = html.escape(code.language) if code.language else ""
        return f'<pre class="bg-gray-800 rounded-lg p-4 overflow-auto mb-4"><code class="language-{language} block">{html.escape(content)}</code></pre>'

