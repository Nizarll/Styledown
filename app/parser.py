from app.markdown import *
import os

MARKDOWN_DIRECTORY = "markdowns"

class Parser:
    def __init__(self, filepath, env):
        filepath += ".md"
        with open(filepath, 'r') as file:
            self.content = file.read()
        self.i = 0
        self.len = len(self.content)
        self.env = env
        self.tokens = []
        self.state = "normal"

    def peek(self, offset=1):
        if self.i + offset > self.len - 1:
            return '\0'
        return self.content[self.i + offset]

    def parse_code(self):
        if self.match("```"):
            self.i += 3
            start = self.i
            while self.i < self.len and self.content[self.i] != '\n':
                self.i += 1
            language = self.content[start:self.i].strip()
            self.i += 1
            start = self.i
            while self.i < self.len and not self.match("```"):
                self.i += 1
            content = self.content[start:self.i].strip()
            self.i += 3
            return MdCode(language=language, content=content)
        return None

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

    def parse_link(self):
        if not self.match("[link "):
            return None
        kind = 0
        self.i += 6
        if self.match("css"):
            kind = 0
            self.i += 3
        elif self.match("file"):
            kind = 1
            self.i += 4
        elif self.match("image"):
            kind = 2
            self.i += 5
        else:
            return None
        
        while self.peek() == ' ':
            self.i += 1

        if self.peek() == '"':
            self.i += 1
        else:
            return None
        start = self.i

        while self.peek != '"' and self.peek() != '\0':
            self.i += 1
        
        if not self.peek() == '"':
            return None

        path = self.content[start:self.i]
        self.i += 1
        return MdLink(kind=kind, content=path)

    def parse(self):
        while self.i < self.len:
            token = None

            if (token := self.parse_list()):
                self.env.append(token)
            elif (token := self.parse_task()):
                self.tokens.append(MdTag(kind=MdKind.TASK, task=token))
            elif (token := self.parse_list()):
                self.tokens.append(MdTag(kind=MdKind.LIST, list=token))
            elif (token := self.parse_heading()):
                self.tokens.append(MdTag(kind=MdKind.HEADING, heading=token))
            elif (token := self.parse_code()):
                self.tokens.append(MdTag(kind=MdKind.CODE, code=token))
            elif (token := self.parse_quote()):
                self.tokens.append(MdTag(kind=MdKind.QUOTE, quote=token))

            if not token:
                self.i += 1  # Move to next character if no token matched

        return self.tokens
