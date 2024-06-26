import tkinter as tk
import os
import json
from tkinter import simpledialog, messagebox
from get_prop_details import GetDetailsFromWeb

# Get the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))

# Main application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialize chrome path and UI
        self.chrome_path = GetDetailsFromWeb.get_chrome_path(self)
        self.UI()
        # Paths for CSV and JSON files
        self.xlsx_file_path = os.path.join(cwd, 'home_details.xlsx')
        self.json_file_path = os.path.join(cwd, 'home_details.json')
        # Remove existing files if they exist
        self.remove_existing()

    def remove_existing(self):
        """Remove existing Excel and JSON files if they exist."""
        if os.path.exists(self.xlsx_file_path):
            os.remove(self.xlsx_file_path)
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)

    def UI(self):
        """Set up the user interface for the application."""
        self.title("Data Scrapper for the Website")
        self.geometry("800x600")

        # Label for website input
        self.label = tk.Label(self, text="Website to fetch data: https://www.realestate.com.au")
        self.label.pack(pady=10)

        # Label for chrome path with option to edit
        self.label = tk.Label(self, text=f"Chrome Path: {self.chrome_path}\nEDIT?")
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        # Buttons for chrome path prompt
        self.yes_button = tk.Button(self.button_frame, text="Yes", command=self.prompt_for_chrome_path)
        self.yes_button.grid(row=0, column=0, padx=5, pady=5)
        self.no_button = tk.Button(self.button_frame, text="No", command=self.no_chrome_path)
        self.no_button.grid(row=0, column=1, padx=5, pady=5)

        # Label for options selection
        self.label_table = tk.Label(self, text="Select options:")
        self.label_table.pack(pady=10)

        # Options for checkboxes
        self.options = [
            "House Name",
            "Property Attributes\n(Bedroom, Bathroom, Parking)",
            "Property Size",
            "Property Type\n(House, land, Town-house)",
            "Price",
            "Bonds(Rent)",
            "Sold Date(Sold)",
            "Property Features",
            "Loan Repay Amount(Estimate)",
            "Description",
            "Floor Plan(URL)",
            "Agent Name",
            "Agent Phone",
            "Agent Organisation",
            "Agent Organisation Address"
        ]

        # Mapping from detailed options to simplified names
        self.option_names = {
            "House Name": "house_name",
            "Property Attributes\n(Bedroom, Bathroom, Parking)": "house_properties_list",
            "Property Size": "property_size",
            "Property Type\n(House, land, Town-house)": "property_type",
            "Price": "property_price",
            "Bonds(Rent)": "property_bonds",
            "Sold Date(Sold)": "sold_date",
            "Property Features": "property_features_item",
            "Loan Repay Amount(Estimate)": "loan_repay_item",
            "Description": "house_details",
            "Floor Plan(URL)": "floorplan_area",
            "Agent Name": "agent_name",
            "Agent Phone": "agent_phone",
            "Agent Organisation": "agent_org",
            "Agent Organisation Address": "agent_org_address"
        }

        # Frame to hold checkboxes
        self.checkbox_frame = tk.Frame(self)
        self.checkbox_frame.pack(pady=10)

        # Variables to hold checkbox states
        self.checkbox_vars = []

        # Create checkboxes in a grid pattern
        columns = 3
        for idx, option in enumerate(self.options):
            var = tk.BooleanVar()
            self.checkbox_vars.append(var)
            checkbox = tk.Checkbutton(self.checkbox_frame, text=option, variable=var, anchor='w', justify='left')
            row, col = divmod(idx, columns)
            col = col * 2  # Skip one cell each time
            checkbox.grid(row=row, column=col, padx=5, pady=5, sticky='w')

        # "Select All" checkbox
        self.select_all_var = tk.BooleanVar()
        total_options = len(self.options)
        select_all_row, select_all_col = divmod(total_options, columns)
        select_all_col = select_all_col * 2  # Skip one cell
        self.select_all_checkbox = tk.Checkbutton(self.checkbox_frame, text="Select All", variable=self.select_all_var, command=self.select_all)
        self.select_all_checkbox.grid(row=select_all_row, column=select_all_col, padx=5, pady=5, sticky='w')

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        # Ensure chrome path is set
        while not GetDetailsFromWeb.get_chrome_path(self):
            self.prompt_for_chrome_path()

    def prompt_for_chrome_path(self):
        """Prompt user to enter the Chrome path."""
        new_chrome_path = simpledialog.askstring("Input", "Please enter the Chrome path:")
        if new_chrome_path:
            self.chrome_path = new_chrome_path
            self.update_chrome_path()
            messagebox.showinfo("Info", "Chrome path updated successfully!")
            self.label.config(text=f"Chrome Path: {self.chrome_path}")

    def no_chrome_path(self):
        """Handle the case when the user clicks 'No'."""
        messagebox.showinfo("Info", "Using existing Chrome path.")

    def update_chrome_path(self):
        """Update the chrome path in the config.json file."""
        config_path = os.path.join(cwd, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r+') as f:
                data = json.load(f)
                data['chrome_path'] = self.chrome_path
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            with open(config_path, 'w') as f:
                data = {'chrome_path': self.chrome_path}
                json.dump(data, f, indent=4)

    def select_all(self):
        """Set all checkboxes to the state of the 'Select All' checkbox."""
        for var in self.checkbox_vars:
            var.set(self.select_all_var.get())

    def update_selection(self):
        """Get the selected items from the checkboxes."""
        selected_options = [self.option_names[self.options[idx]] for idx, var in enumerate(self.checkbox_vars) if var.get()]
        print(f"Selected Options: {selected_options}")

    def submit(self):
        """Submit the selected options."""
        selected_options = [self.option_names[self.options[idx]] for idx, var in enumerate(self.checkbox_vars) if var.get()]
        GetDetailsFromWeb(selected_options)

# Run the application
if __name__ == "__main__":
    home_details = []
    app = App()
    try:
        app.mainloop()
    except Exception as e:
        print("TK error here:", e)
