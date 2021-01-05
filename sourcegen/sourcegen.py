import os
import re
from functools import total_ordering

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

    @total_ordering
    class Marker:
        def __init__(self, start, end, indent):
            self.start = start
            self.end = end
            self.indent = indent

            self.text = None

        def __eq__(self, other):
            return self.start == other.start and self.end == other.end

        def __lt__(self, other):
            return self.start < other.start

        def set_text(self, text, delimiter: str = None, wrap_width: int = None):
            if delimiter is not None:
                assert isinstance(delimiter, str)
                delimiter = delimiter.replace(os.linesep, (os.linesep + self.indent))
                text = delimiter.join(text)

            if wrap_width is not None:
                assert isinstance(wrap_width, int)
                text = utils.wrap(text, wrap_width - len(self.indent), self.indent)                

            self.text = text
        
    def __init__(self, target_file, verbose=False):
        self.target_file = target_file
        self.verbose = verbose

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

                            self.markers[name] = self.Marker(start, i, indent)

                            if self.verbose:
                                print(
                                    f"Adding marker:"
                                    f"\n\tstart:  {start}"
                                    f"\n\tend:    {i}"
                                    f"\n\tindent: '{indent}' ({len(indent)})"
                                )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        markers = iter(sorted(self.markers.values()))
        marker = next(markers)
        new_lines = []

        i = 0
        while i < len(self.lines):
            if i < marker.start:
                new_lines.append(self.lines[i])
                i += 1
            else:
                new_lines.extend(
                    (
                        self.lines[i],
                        marker.indent,
                        marker.text,
                        os.linesep,
                        self.lines[marker.end],
                    )
                )
                i = marker.end + 1
                try:
                    marker = next(markers)
                except StopIteration:
                    new_lines.extend(self.lines[i:])
                    break

        new_text = "".join(new_lines)
        old_text = "".join(self.lines)

        if new_text != old_text:
            with open(self.target_file, "w") as file:
                file.write(new_text)

    def __getitem__(self, name):
        return self.markers[name]
