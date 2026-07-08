import os
from datetime import datetime, timedelta
from library import Library

def display_dashboard(library):
    stats = library.get_statistics()
    overdue_list, _ = library.get_overdue_info()
    print("\n" + "=" * 40)
    print("           Library Dashboard")
    print("=" * 40)
    print(f"  Total Books Registered  : {stats['total_books']}")
    print(f"  Available Books         : {stats['available_books']}")
    print(f"  Issued Books            : {stats['issued_books']}")
    print(f"  Registered Members      : {stats['total_members']}")
    print(f"  Overdue Books           : {len(overdue_list)}")
    print("=" * 40)

def main():
    library = Library()
    
    # Show dashboard once at start
    display_dashboard(library)

    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Dashboard")
        print("2. Book Management")
        print("3. Member Management")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Search & Recommendations")
        print("7. Reports & Activity Log")
        print("8. Statistics & Analytics")
        print("9. Exit")
        
        choice = input("Enter choice (1-9): ").strip()
        
        if choice == "1":
            display_dashboard(library)
            
        elif choice == "2":
            print("\n--- Book Management ---")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. Update Book Details")
            print("4. View All Books")
            sub = input("Enter option (1-4): ").strip()
            
            if sub == "1":
                bid = input("Enter Book ID (e.g. B06): ").strip()
                if not bid:
                    print("Error: Book ID cannot be empty.")
                    continue
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                print("Categories: " + ", ".join(library.categories))
                cat = input("Enter Category (choose existing or type a new one): ").strip()
                if not title or not author or not cat:
                    print("Error: Book details cannot be empty.")
                    continue
                library.add_book(bid, title, author, cat)
                
            elif sub == "2":
                bid = input("Enter Book ID to remove: ").strip()
                library.remove_book(bid)
                
            elif sub == "3":
                bid = input("Enter Book ID to update: ").strip()
                if bid not in library.books:
                    print("Error: Book not found.")
                    continue
                title = input("Enter new Title (Enter to skip): ").strip()
                author = input("Enter new Author (Enter to skip): ").strip()
                cat = input("Enter new Category (Enter to skip): ").strip()
                library.update_book(bid, title, author, cat)
                
            elif sub == "4":
                if not library.books:
                    print("No books registered.")
                else:
                    print("\n" + "-" * 60)
                    for b in library.books.values():
                        status = "Available" if b.is_available else "Issued"
                        print(f"[{b.book_id}] {b.title:<25} by {b.author:<15} | Cat: {b.category:<15} | {status}")
                    print("-" * 60)
                    
        elif choice == "3":
            print("\n--- Member Management ---")
            print("1. Register Member")
            print("2. View Member Profile")
            print("3. View All Members")
            sub = input("Enter option (1-3): ").strip()
            
            if sub == "1":
                mid = input("Enter Member ID (e.g. M05): ").strip()
                if not mid:
                    print("Error: Member ID cannot be empty.")
                    continue
                name = input("Enter Full Name: ").strip()
                if not name:
                    print("Error: Name cannot be empty.")
                    continue
                library.register_member(mid, name)
                
            elif sub == "2":
                mid = input("Enter Member ID: ").strip()
                if mid not in library.members:
                    print("Error: Member not found.")
                    continue
                m = library.members[mid]
                print(f"\nMember Profile: {m.name} ({m.member_id})")
                print(f"Total Borrowed Historically: {len(m.borrowing_history)}")
                print("Currently Borrowed Books:")
                if not m.borrowed_books:
                    print("  None")
                else:
                    for bid, due_date in m.borrowed_books.items():
                        title = library.books[bid].title if bid in library.books else "Unknown"
                        print(f"  - [{bid}] {title} (Due: {due_date})")
                        
            elif sub == "3":
                if not library.members:
                    print("No registered members.")
                else:
                    print("\n" + "-" * 50)
                    for m in library.members.values():
                        print(f"[{m.member_id}] {m.name:<20} | Borrowed: {len(m.borrowed_books)}")
                    print("-" * 50)
                    
        elif choice == "4":
            bid = input("Enter Book ID to issue: ").strip()
            mid = input("Enter Member ID: ").strip()
            library.issue_book(bid, mid)
            
        elif choice == "5":
            bid = input("Enter Book ID to return: ").strip()
            mid = input("Enter Member ID: ").strip()
            library.return_book(bid, mid)
            
        elif choice == "6":
            print("\n--- Search & Recommendations ---")
            print("1. Search Books (Partial match on ID, Title, Author, Category)")
            print("2. Get Recommendations by Category")
            sub = input("Enter option (1-2): ").strip()
            
            if sub == "1":
                query = input("Enter search query: ").strip()
                results = library.search_books(query)
                if not results:
                    print("No matching books found.")
                else:
                    print(f"\nFound {len(results)} match(es):")
                    for b in results:
                        status = "Available" if b.is_available else "Issued"
                        print(f"  [{b.book_id}] {b.title} by {b.author} ({b.category}) - {status}")
            elif sub == "2":
                print("Available categories: " + ", ".join(library.categories))
                cat = input("Enter Category: ").strip()
                recs = library.get_recommendations(cat)
                if not recs:
                    print("No books found in this category.")
                else:
                    print(f"\nRecommended Books in '{cat}':")
                    for b in recs:
                        status = "Available" if b.is_available else "Issued (Unavailable)"
                        print(f"  [{b.book_id}] {b.title} by {b.author} - {status}")
                        
        elif choice == "7":
            print("\n--- Reports & Activity Log ---")
            print("1. Export System Report to 'library_report.txt'")
            print("2. Check Overdue Books & Fines")
            print("3. View System Activity Log")
            sub = input("Enter option (1-3): ").strip()
            
            if sub == "1":
                library.export_report()
                print("Report successfully exported to 'library_report.txt'.")
            elif sub == "2":
                overdue, total_fine = library.get_overdue_info()
                if not overdue:
                    print("No overdue books found.")
                else:
                    print("\n--- OVERDUE LIST ---")
                    for item in overdue:
                        print(f"Book: {item['book_title']} ({item['book_id']}) | Member: {item['member_name']} ({item['member_id']}) | Due: {item['due_date']} | Fine: ₹{item['fine']}")
                    print(f"Total Outstanding Fines: ₹{total_fine}")
            elif sub == "3":
                if not library.transactions:
                    print("No activity recorded yet.")
                else:
                    print("\n--- Activity Log (Last 15) ---")
                    for t in library.transactions[-15:]:
                        dur_info = f" | Duration: {t['borrow_duration_days']} days" if "borrow_duration_days" in t else ""
                        print(f"[{t['date']} {t['time']}] {t['action']:<18} | Book: {t['book']:<25} | Member: {t['member']}{dur_info}")
                        
        elif choice == "8":
            stats = library.get_statistics()
            print("\n--- Library Statistics & Analytics ---")
            print(f"  Total Books Registered  : {stats['total_books']}")
            print(f"  Available Books         : {stats['available_books']}")
            print(f"  Issued Books            : {stats['issued_books']}")
            print(f"  Total Registered Members: {stats['total_members']}")
            print(f"  Average Books / Member  : {stats['avg_books_per_member']}")
            print("-" * 40)
            print("  --- READING ANALYTICS ---")
            print(f"  Most Borrowed Category  : {stats['popular_category']}")
            print(f"  Most Borrowed Book      : {stats['most_borrowed_book']}")
            print(f"  Most Active Member      : {stats['active_member']}")
            print(f"  Average Borrow Duration : {stats['avg_duration']} days")
            print("-" * 40)
            
        elif choice == "9":
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid input. Please choose a number between 1 and 9.")

if __name__ == "__main__":
    main()
