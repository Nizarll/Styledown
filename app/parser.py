from app.markdown import MdTag, MdKind, MdHeading, MdTask, MdList, MdQuote, TaskKind
import os

MARKDOWN_DIRECTORY = "markdowns"

class Parser:
    def __init__(self, filepath):
        filepath += ".md"
        with open(filepath, 'r') as file:
            self.content = file.read()
        self.i = 0
        self.len = len(self.content)
        self.tokens = []
        self.state = "normal"

    def peek(self, offset=1):
        if self.i + offset > self.len - 1:
            return '\0'
        return self.content[self.i + offset]

    def peek(self, offset=1):
        if self.i + offset > self.len - 1:
            return '\0'
        return self.content[self.i + offset]

    def match(self, text):
        if self.i + len(text) > self.len:
            return False
        for j in range(len(text)):
            if self.content[self.i + j] != text[j]:
                return False
        return True

    def parse_task(self):
        if self.match("[ ]"):
            self.i += 4
            description = self._parse_task_description()
            return MdTask(kind=TaskKind.CHECKBOX_EMPTY, description=description)

        elif self.match("[x]"):
            self.i += 4
            description = self._parse_task_description()
            return MdTask(kind=TaskKind.CHECKBOX_FILLED, description=description)

        elif self.match("[!]"):
            self.i += 4
            description = self._parse_task_description()
            return MdTask(kind=TaskKind.WARNING, description=description)

        elif self.match("[e]"):
            self.i += 4
            description = self._parse_task_description()
            return MdTask(kind=TaskKind.EMERGENCY, description=description)

        return None

    def _parse_task_description(self):
        start = self.i
        while self.i < self.len and self.content[self.i] not in ['\n', '\r']:
            self.i += 1
        return self.content[start:self.i]

    def parse_list(self):
        if self.match("- ") or self.match("* "):
            self.i += 2
            start = self.i
            while self.i < self.len and self.content[self.i] not in ['\n', '\r']:
                self.i += 1
            return MdList(items=[self.content[start:self.i]])
        return None

    def parse_heading(self):
        level = 0
        while self.i < self.len and self.content[self.i] == '#':
            level += 1
            self.i += 1
        if level > 0:
            if self.content[self.i] == ' ':
                self.i += 1
            start = self.i
            while self.i < self.len and self.content[self.i] not in ['\n', '\r']:
                self.i += 1
            return MdHeading(level=level, content=self.content[start:self.i])
        return None

    def parse_quote(self):
        if self.match("> "):
            self.i += 2
            start = self.i
            while self.i < self.len and self.content[self.i] not in ['\n', '\r']:
                self.i += 1
            return MdQuote(level=1, content=self.content[start:self.i])
        return None

    def parse(self):
        while self.i < self.len:
            token = None

            if (token := self.parse_task()):
                self.tokens.append(MdTag(kind=MdKind.TASK, task=token))
            elif (token := self.parse_list()):
                self.tokens.append(MdTag(kind=MdKind.LIST, list=token))
            elif (token := self.parse_heading()):
                self.tokens.append(MdTag(kind=MdKind.HEADING, heading=token))
            elif (token := self.parse_quote()):
                self.tokens.append(MdTag(kind=MdKind.QUOTE, quote=token))

            if not token:
                self.i += 1  # Move to next character if no token matched

        return self.tokens
