from contact import Contact
import csv

class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email, category):
        contact = Contact(name, phone, email, category)
        self.contacts.append(contact)

    def delete_contact(self, name):
        self.contacts = [contact for contact in self.contacts if contact.name != name]

    def search_contacts(self, search_term):
        return [contact for contact in self.contacts if search_term.lower() in contact.name.lower() or search_term.lower() in contact.phone.lower() or search_term.lower() in contact.email.lower()]

    def edit_contact(self, old_name, new_name, new_phone, new_email, new_category):
        for contact in self.contacts:
            if contact.name == old_name:
                contact.name = new_name
                contact.phone = new_phone
                contact.email = new_email
                contact.category = new_category

    def import_contacts(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 4:
                    self.add_contact(row[0], row[1], row[2], row[3])

    def export_contacts(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for contact in self.contacts:
                writer.writerow([contact.name, contact.phone, contact.email, contact.category])