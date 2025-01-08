import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class BaseBook(ABC):
    DISPLAY_TYPES = ("console", "reverse")

    def check_type(self, command,  type_to_check: str):
        if type_to_check not in self.DISPLAY_TYPES:
            raise ValueError(f"Unknown {command} type: {type_to_check}")

    @abstractmethod
    def display(self, display_type):
        ...

    @abstractmethod
    def display_console(self):
        ...

    @abstractmethod
    def display_reverse(self):
        ...

    @abstractmethod
    def print(self, print_type):
        ...

    @abstractmethod
    def print_console(self):
        ...

    @abstractmethod
    def print_reverse(self):
        ...


class Book(BaseBook):

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def display(self, display_type: str) -> None:
        self.check_type("display", display_type)

        getattr(self, f"display_{display_type}")()

    def display_console(self):
        print(self.content)

    def display_reverse(self):
        print(self.content[::-1])

    def print(self, print_type):
        self.check_type("print", print_type)

        getattr(self, f"print_{print_type}")()

    def print_console(self):
        print(f"Printing the book: {self.title}...")
        print(self.content)

    def print_reverse(self):
        print(f"Printing the book in reverse: {self.title}...")
        print(self.content[::-1])

    def serialize(self, serialize_type: str) -> str:
        if serialize_type == "json":
            return json.dumps({"title": self.title, "content": self.content})
        elif serialize_type == "xml":
            root = ET.Element("book")
            title = ET.SubElement(root, "title")
            title.text = self.title
            content = ET.SubElement(root, "content")
            content.text = self.content
            return ET.tostring(root, encoding="unicode")
        else:
            raise ValueError(f"Unknown serialize type: {serialize_type}")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            getattr(book, f"{cmd}_{method_type}")()
        elif cmd == "print":
            getattr(book, f"{cmd}_{method_type}")()
        elif cmd == "serialize":
            return book.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(
        main(sample_book,
             [
                 ("display", "reverse"),
                 ("serialize", "xml")
             ]
             )
    )
