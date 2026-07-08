class Book:
    """Represents a book in the library system."""
    def __init__(self, book_id, title, author, category, is_available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.is_available = is_available

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "is_available": self.is_available
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["category"],
            data.get("is_available", True)
        )


class Member:
    """Represents a registered library member."""
    def __init__(self, member_id, name, borrowed_books=None, borrowing_history=None):
        self.member_id = member_id
        self.name = name
        # borrowed_books: dict mapping book_id -> issue_date_str (e.g. {"B01": "2026-07-08"})
        self.borrowed_books = borrowed_books if borrowed_books is not None else {}
        # borrowing_history: list of book_ids that were ever borrowed
        self.borrowing_history = borrowing_history if borrowing_history is not None else []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books,
            "borrowing_history": self.borrowing_history
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["member_id"],
            data["name"],
            data.get("borrowed_books", {}),
            data.get("borrowing_history", [])
        )
