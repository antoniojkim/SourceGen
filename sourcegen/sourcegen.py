import os
import re

from . import utils

comment_styles = {
    ".py": "#",
    ".c": "//",
    ".cc": "//",
    ".cpp": "//",
    ".h": "//",
    ".hh": "//",
    ".hpp": "//",
}


class SourceGenerator:
    def __init__(self, target_file):
        self.target_file = target_file

    def __enter__(self):
        filename, ext = os.path.splitext(self.target_file)
        if ext not in comment_styles:
            raise RuntimeError(f"Unsupported file extension: {ext}")

        comment_style = comment_styles[ext]

        with open(self.target_file) as file:
            self.lines = file.readlines()

        self.markers = {}
        sourcegen = None
        for i, line in enumerate(self.lines):
            if line.lstrip().startswith(comment_style):
                marker = line.split(comment_style)
                indent = marker[0]
                command = marker[1].strip().split(" ")
                print(command)

                if command[0].lower() in ("begin", "end"):
                    if command[1].lower() == "sourcegen":
                        if command[0].lower() == "begin":
                            assert sourcegen is None, "Cannot nest sourcegen statements"
                            sourcegen = (i, indent, command[2])
                        elif command[0].lower() == "end":
                            assert sourcegen is not None, "Invalid sourcegen statement"
                            start, indent, name = sourcegen
                            sourcegen = None

                            if name in self.markers:
                                raise ValueError(f"Non-unique name found: {name}")

                            self.markers[name] = (start, i, indent, "")

        print(self.markers)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        markers = iter(sorted(self.markers.values()))
        start, end, _, text = next(markers)
        new_lines = []

        i = 0
        while i < len(self.lines):
            if i < start:
                new_lines.append(self.lines[i])
                i += 1
            else:
                new_lines.extend((
                    self.lines[i],
                    text,
                    os.linesep,
                    self.lines[end],
                ))
                i = end + 1
                try:
                    start, end, _, text = next(markers)
                except StopIteration:
                    new_lines.extend(self.lines[i:])
                    break

        new_text = "".join(new_lines)
        old_text = "".join(self.lines)

        if new_text != old_text:
            with open(self.target_file, "w") as file:
                file.write(new_text)

    def generate(self, name, value, wrap=False, wrap_width=80):
        assert name in self.markers

        start, end, indent, prev = self.markers[name]

        if wrap:
            value = utils.wrap(value, wrap_width - len(indent), indent)

        self.markers[name] = (start, end, indent, indent + value)
