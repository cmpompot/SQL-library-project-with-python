import csv
import random
from datetime import datetime, timedelta
import uuid

#lists of data for generating realistic books
categories = [
    'Fiction', 'Mystery', 'Thriller', 'Science Fiction', 'Fantasy', 'Romance',
    'Historical Fiction', 'Horror', 'Biography', 'Autobiography', 'Memoir',
    'Self-Help', 'Business', 'History', 'Science', 'Travel', 'Cooking',
    'Art', 'Philosophy', 'Religion', 'Health', 'Psychology', 'Education',
    'Technology', 'Poetry', 'Drama', 'Classic', 'Young Adult', 'Children'
]

first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas',
               'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

publishers = [
    'Penguin Random House', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Hachette Book Group',
    'Scholastic', 'Pearson', 'McGraw-Hill', 'Houghton Mifflin', 'Wiley',
    'Oxford University Press', 'Cambridge University Press', 'Elsevier', 'Springer', 'Taylor & Francis'
]

book_titles = [
    'The Shadow in the Attic', 'Echoes of Tomorrow', 'Whispers in the Dark', 'Secrets of the Ocean',
    'Beyond the Horizon', 'The Last Guardian', 'Eternal Flame', 'Silent Echo', 'Fading Memories',
    'The Hidden Kingdom', 'Crimson Dawn', 'Midnight Rain', 'The Forgotten City', 'Sands of Time',
    'Winter\'s Heart', 'Summer\'s End', 'Autumn Leaves', 'Spring Awakening', 'The Crystal Cave',
    'The Iron Fortress', 'The Golden Compass', 'The Silver Lining', 'The Bronze Key', 'The Obsidian Tower'
]

adjectives = ['Great', 'Secret', 'Hidden', 'Lost', 'Forgotten', 'Dark', 'Mysterious', 'Ancient', 'Eternal', 'Final']
nouns = ['Quest', 'Journey', 'Legacy', 'Empire', 'Kingdom', 'World', 'City', 'Forest', 'Ocean', 'Mountain']

#generate more book titles by combining elements
for adj in adjectives:
    for noun in nouns:
        book_titles.append(f"The {adj} {noun}")

#generate author names
authors = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(100)]

#generate ISBNs
def generate_isbn():
    return f"978-{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}-{random.randint(10000, 99999)}-{random.randint(0, 9)}"

#generate publication years 
def generate_published_year():
    return random.randint(1800, 2023)

#generate purchase dates 
def generate_purchase_date():
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2023, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

#generate purchase prices 
def generate_purchase_price():
    return round(random.uniform(5, 50), 2)

#generate rental prices 
def generate_rental_price():
    return round(random.uniform(1, 10), 2)

#generate shelf locations
def generate_shelf_location():
    sections = ['FIC', 'MYS', 'SCI', 'FAN', 'BIO', 'HIS', 'ART', 'SCI', 'BUS', 'TRA']
    return f"{random.choice(sections)}-{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 20)}"

#generate status with weighted probability (mostly Available)
def generate_status():
    return random.choices(
        ['Available', 'Issued', 'Reserved', 'Under Maintenance'],
        weights=[0.7, 0.2, 0.08, 0.02]
    )[0]

num_books =100

with open('library_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'ISBN', 'Book_title', 'Category', 'Rental_Price', 'Status', 
        'Author', 'Publisher', 'Published_year', 'Purchase_date', 
        'Purchase_price', 'Branch_no', 'Shelf_location'
    ]
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    #generation
    for i in range(num_books):
        writer.writerow({
            'ISBN': generate_isbn(),
            'Book_title': random.choice(book_titles),
            'Category': random.choice(categories),
            'Rental_Price': generate_rental_price(),
            'Status': generate_status(),
            'Author': random.choice(authors),
            'Publisher': random.choice(publishers),
            'Published_year': generate_published_year(),
            'Purchase_date': generate_purchase_date(),
            'Purchase_price': generate_purchase_price(),
                'Branch_no': random.randint(1, 3),
            'Shelf_location': generate_shelf_location()
        })

print(f"Successfully generated {num_books} book records in 'library_books.csv'")