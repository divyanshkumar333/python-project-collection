import os
import json
from datetime import datetime, timedelta
from models import Book, Member

class Library:
    """Manages the books, members, transactions, and analytics of the library."""
    def __init__(self, file_path="library.json"):
        self.file_path = file_path
        self.books = {}
        self.members = {}
        self.transactions = []
        self.categories = [
            "AI & Data Science", "Programming", "Cyber Security",
            "Web Development", "Fiction", "History", "Self Help"
        ]
        self.settings = {
            "fine_per_day": 10,
            "borrow_period_days": 14
        }
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.save_data()
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = {bid: Book.from_dict(b) for bid, b in data.get("books", {}).items()}
                self.members = {mid: Member.from_dict(m) for mid, m in data.get("members", {}).items()}
                self.transactions = data.get("transactions", [])
                self.categories = data.get("categories", self.categories)
                self.settings = data.get("settings", self.settings)
        except (json.JSONDecodeError, KeyError, PermissionError):
            print("Error loading database. Starting with a reset library system.")

    def save_data(self):
        data = {
            "books": {bid: b.to_dict() for bid, b in self.books.items()},
            "members": {mid: m.to_dict() for mid, m in self.members.items()},
            "transactions": self.transactions,
            "categories": self.categories,
            "settings": self.settings
        }
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("Error: Permission denied when writing to database.")

    def log_activity(self, action, book_info, member_info, extra_details=None):
        now = datetime.now()
        log_entry = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "action": action,
            "book": book_info,
            "member": member_info
        }
        if extra_details:
            log_entry.update(extra_details)
        self.transactions.append(log_entry)
        self.save_data()

    def add_book(self, book_id, title, author, category):
        if book_id in self.books:
            print("Error: Book ID already exists.")
            return False
        if category not in self.categories:
            self.categories.append(category)
        book = Book(book_id, title, author, category)
        self.books[book_id] = book
        self.log_activity("Book Added", f"{title} ({book_id})", "N/A")
        print(f"Book '{title}' successfully added.")
        return True

    def remove_book(self, book_id):
        if book_id not in self.books:
            print("Error: Book not found.")
            return False
        book = self.books[book_id]
        if not book.is_available:
            print("Error: Cannot remove an issued book.")
            return False
        del self.books[book_id]
        self.log_activity("Book Removed", f"{book.title} ({book_id})", "N/A")
        print(f"Book '{book.title}' successfully removed.")
        return True

    def update_book(self, book_id, title, author, category):
        if book_id not in self.books:
            print("Error: Book not found.")
            return False
        book = self.books[book_id]
        if title: book.title = title
        if author: book.author = author
        if category:
            if category not in self.categories:
                self.categories.append(category)
            book.category = category
        self.save_data()
        print(f"Book ID '{book_id}' details successfully updated.")
        return True

    def register_member(self, member_id, name):
        if member_id in self.members:
            print("Error: Member ID already exists.")
            return False
        member = Member(member_id, name)
        self.members[member_id] = member
        self.log_activity("Member Registered", "N/A", f"{name} ({member_id})")
        print(f"Member '{name}' successfully registered.")
        return True

    def issue_book(self, book_id, member_id):
        if book_id not in self.books:
            print("Error: Book not found.")
            return False
        if member_id not in self.members:
            print("Error: Member not found.")
            return False
        book = self.books[book_id]
        member = self.members[member_id]
        if not book.is_available:
            print("Error: Book is already issued to someone else.")
            return False
        
        issue_date_str = datetime.now().strftime("%Y-%m-%d")
        
        book.is_available = False
        member.borrowed_books[book_id] = issue_date_str
        if book_id not in member.borrowing_history:
            member.borrowing_history.append(book_id)
        
        self.log_activity("Book Issued", f"{book.title} ({book_id})", f"{member.name} ({member_id})")
        
        due_date = datetime.now() + timedelta(days=self.settings.get("borrow_period_days", 14))
        print(f"Book '{book.title}' issued to {member.name}. Due Date: {due_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, book_id, member_id):
        if member_id not in self.members:
            print("Error: Member not found.")
            return False
        member = self.members[member_id]
        if book_id not in member.borrowed_books:
            print("Error: This book was not issued to this member.")
            return False
        
        issue_date_str = member.borrowed_books.pop(book_id)
        if book_id in self.books:
            self.books[book_id].is_available = True
            book_title = self.books[book_id].title
        else:
            book_title = "Unknown Book"

        # Calculate duration and fine
        issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
        today = datetime.now()
        duration_days = (today.date() - issue_date.date()).days
        
        due_date = issue_date + timedelta(days=self.settings.get("borrow_period_days", 14))
        fine = self.calculate_fine(due_date)
        
        self.log_activity(
            "Book Returned", 
            f"{book_title} ({book_id})", 
            f"{member.name} ({member_id})",
            extra_details={"borrow_duration_days": max(0, duration_days)}
        )
        
        print(f"Book '{book_title}' returned successfully.")
        if fine > 0:
            print(f"Overdue fine to pay: ₹{fine}")
        return True

    def calculate_fine(self, due_date):
        today = datetime.now().date()
        due = due_date.date()
        if today > due:
            return (today - due).days * self.settings.get("fine_per_day", 10)
        return 0

    def get_overdue_info(self):
        overdue_items = []
        total_fine = 0
        for mid, member in self.members.items():
            for bid, issue_date_str in member.borrowed_books.items():
                issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
                due_date = issue_date + timedelta(days=self.settings.get("borrow_period_days", 14))
                fine = self.calculate_fine(due_date)
                if fine > 0:
                    book_title = self.books[bid].title if bid in self.books else "Unknown Book"
                    overdue_items.append({
                        "member_id": mid,
                        "member_name": member.name,
                        "book_id": bid,
                        "book_title": book_title,
                        "due_date": due_date.strftime("%Y-%m-%d"),
                        "fine": fine
                    })
                    total_fine += fine
        return overdue_items, total_fine

    def search_books(self, query):
        query = query.lower()
        results = []
        for book in self.books.values():
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.category.lower() or 
                query in book.book_id.lower()):
                results.append(book)
        return results

    def get_recommendations(self, category):
        """Recommends books in the same category, prioritizing available ones."""
        matching_books = [b for b in self.books.values() if b.category.lower() == category.lower()]
        # Sort so that available books come first
        matching_books.sort(key=lambda x: not x.is_available)
        return matching_books[:5]

    def get_statistics(self):
        total_books = len(self.books)
        available_books = sum(1 for b in self.books.values() if b.is_available)
        issued_books = total_books - available_books
        total_members = len(self.members)
        
        # Most popular category calculation (based on borrowing history)
        category_counts = {}
        book_counts = {}
        for member in self.members.values():
            for bid in member.borrowing_history:
                book_counts[bid] = book_counts.get(bid, 0) + 1
                if bid in self.books:
                    cat = self.books[bid].category
                    category_counts[cat] = category_counts.get(cat, 0) + 1
        
        popular_category = max(category_counts, key=category_counts.get) if category_counts else "None"
        
        # Most borrowed book
        most_borrowed_book = "None"
        if book_counts:
            mb_id = max(book_counts, key=book_counts.get)
            if mb_id in self.books:
                most_borrowed_book = f"{self.books[mb_id].title} ({mb_id}) - Borrowed {book_counts[mb_id]} times"
        
        # Most active member
        active_member = "None"
        max_borrows = 0
        for member in self.members.values():
            if len(member.borrowing_history) > max_borrows:
                max_borrows = len(member.borrowing_history)
                active_member = f"{member.name} ({member.member_id})"
                
        # Average borrow duration calculation
        durations = [t.get("borrow_duration_days") for t in self.transactions if "borrow_duration_days" in t]
        avg_duration = round(sum(durations) / len(durations), 1) if durations else 0.0
        
        avg_books = total_books / total_members if total_members > 0 else 0.0
        
        return {
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_members": total_members,
            "popular_category": popular_category,
            "most_borrowed_book": most_borrowed_book,
            "active_member": active_member,
            "avg_books_per_member": round(avg_books, 2),
            "avg_duration": avg_duration
        }

    def export_report(self, filepath="library_report.txt"):
        stats = self.get_statistics()
        overdue_list, total_fine = self.get_overdue_info()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("========================================================\n")
            f.write("                 LIBRARY MANAGEMENT SYSTEM REPORT       \n")
            f.write(f"                 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("========================================================\n\n")
            
            f.write("-------------------- METRICS & STATS --------------------\n")
            f.write(f"Total Books Registered  : {stats['total_books']}\n")
            f.write(f"Books Available         : {stats['available_books']}\n")
            f.write(f"Books Issued            : {stats['issued_books']}\n")
            f.write(f"Total Members           : {stats['total_members']}\n")
            f.write(f"Most Borrowed Category  : {stats['popular_category']}\n")
            f.write(f"Most Borrowed Book      : {stats['most_borrowed_book']}\n")
            f.write(f"Most Active Member      : {stats['active_member']}\n")
            f.write(f"Average Borrow Duration : {stats['avg_duration']} days\n")
            f.write(f"Average Books / Member  : {stats['avg_books_per_member']}\n\n")
            
            f.write("-------------------- REGISTERED BOOKS -------------------\n")
            for b in self.books.values():
                status = "Available" if b.is_available else "Issued"
                f.write(f"ID: {b.book_id:<6} | {b.title:<30} | {b.author:<20} | Category: {b.category:<20} | Status: {status}\n")
            f.write("\n")
            
            f.write("-------------------- REGISTERED MEMBERS -----------------\n")
            for m in self.members.values():
                f.write(f"ID: {m.member_id:<6} | Name: {m.name:<25} | Currently Borrowed: {len(m.borrowed_books):<2} | Total History: {len(m.borrowing_history)}\n")
            f.write("\n")
            
            f.write("-------------------- CURRENT ISSUES ---------------------\n")
            issued_count = 0
            for m in self.members.values():
                for bid, issue_date_str in m.borrowed_books.items():
                    title = self.books[bid].title if bid in self.books else "Unknown"
                    f.write(f"Book ID: {bid:<6} | Title: {title:<30} | Borrower: {m.name:<20} | Issued on: {issue_date_str}\n")
                    issued_count += 1
            if issued_count == 0:
                f.write("No books currently issued.\n")
            f.write("\n")
            
            f.write("-------------------- OVERDUE SUMMARY & FINES ------------\n")
            if not overdue_list:
                f.write("No overdue books. Total Outstanding Fine: ₹0\n")
            else:
                for item in overdue_list:
                    f.write(f"Book: {item['book_title']:<25} ({item['book_id']}) | Borrower: {item['member_name']:<20} | Fine: ₹{item['fine']:<5} | Due: {item['due_date']}\n")
                f.write(f"Total Outstanding Fine: ₹{total_fine}\n")
            f.write("========================================================\n")
