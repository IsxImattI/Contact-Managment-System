import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from contactmanager import ContactManager

class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Management System")
        
        self.selected_contact_name = None

        # Create frames
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # Add contact form
        self.lbl_name = tk.Label(self.frame, text="Name")
        self.lbl_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.lbl_phone = tk.Label(self.frame, text="Phone")
        self.lbl_phone.grid(row=1, column=0, padx=10, pady=5)
        self.entry_phone = tk.Entry(self.frame)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=5)

        self.lbl_email = tk.Label(self.frame, text="Email")
        self.lbl_email.grid(row=2, column=0, padx=10, pady=5)
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        self.lbl_category = tk.Label(self.frame, text="Category")
        self.lbl_category.grid(row=3, column=0, padx=10, pady=5)
        self.entry_category = tk.Entry(self.frame)
        self.entry_category.grid(row=3, column=1, padx=10, pady=5)

        self.btn_add_contact = tk.Button(self.frame, text="Add Contact", command=self.add_contact)
        self.btn_add_contact.grid(row=4, columnspan=2, pady=10)

        # Contact list and operations
        self.contact_list = tk.Listbox(self.frame, width=50, height=10)
        self.contact_list.grid(row=5, columnspan=2, pady=10)
        self.contact_list.bind('<<ListboxSelect>>', self.on_select)

        self.btn_edit_contact = tk.Button(self.frame, text="Edit Contact", command=self.edit_contact)
        self.btn_edit_contact.grid(row=6, column=0, pady=10)

        self.btn_delete_contact = tk.Button(self.frame, text="Delete Contact", command=self.delete_contact)
        self.btn_delete_contact.grid(row=6, column=1, pady=10)

        self.lbl_search = tk.Label(self.frame, text="Search")
        self.lbl_search.grid(row=7, column=0, padx=10, pady=5)
        self.entry_search = tk.Entry(self.frame)
        self.entry_search.grid(row=7, column=1, padx=10, pady=5)
        self.entry_search.bind('<KeyRelease>', self.search_contacts)

        self.btn_import_contacts = tk.Button(self.frame, text="Import Contacts", command=self.import_contacts)
        self.btn_import_contacts.grid(row=8, column=0, pady=10)

        self.btn_export_contacts = tk.Button(self.frame, text="Export Contacts", command=self.export_contacts)
        self.btn_export_contacts.grid(row=8, column=1, pady=10)

    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        category = self.entry_category.get()
        if name and phone and email and category:
            self.manager.add_contact(name, phone, email, category)
            self.update_contact_list()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "All fields must be filled")

    def delete_contact(self):
        selected_contact = self.contact_list.get(tk.ACTIVE)
        if selected_contact:
            name = selected_contact.split(' - ')[0]
            self.manager.delete_contact(name)
            self.update_contact_list()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "No contact selected")

    def edit_contact(self):
        if self.selected_contact_name:
            new_name = self.entry_name.get()
            new_phone = self.entry_phone.get()
            new_email = self.entry_email.get()
            new_category = self.entry_category.get()
            if new_name and new_phone and new_email and new_category:
                self.manager.edit_contact(self.selected_contact_name, new_name, new_phone, new_email, new_category)
                self.update_contact_list()
                self.clear_entries()
                self.selected_contact_name = None
            else:
                messagebox.showerror("Error", "All fields must be filled")
        else:
            messagebox.showerror("Error", "No contact selected for editing")

    def search_contacts(self, event):
        search_term = self.entry_search.get()
        results = self.manager.search_contacts(search_term)
        self.contact_list.delete(0, tk.END)
        for contact in results:
            self.contact_list.insert(tk.END, f"{contact.name} - {contact.phone} - {contact.email} - {contact.category}")

    def import_contacts(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.manager.import_contacts(filename)
            self.update_contact_list()

    def export_contacts(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.manager.export_contacts(filename)

    def update_contact_list(self):
        self.contact_list.delete(0, tk.END)
        for contact in self.manager.contacts:
            self.contact_list.insert(tk.END, f"{contact.name} - {contact.phone} - {contact.email} - {contact.category}")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)

    def on_select(self, event):
        selected_contact = self.contact_list.get(tk.ACTIVE)
        if selected_contact:
            name, phone, email, category = selected_contact.split(' - ')
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(tk.END, name)
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(tk.END, phone)
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(tk.END, email)
            self.entry_category.delete(0, tk.END)
            self.entry_category.insert(tk.END, category)
            self.selected_contact_name = name

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
