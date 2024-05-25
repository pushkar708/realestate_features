import tkinter as tk
import os
import json
from tkinter import simpledialog, messagebox
from get_prop_details import GetDetailsFromWeb
cwd = os.path.dirname(os.path.abspath(__file__))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.chrome_path=GetDetailsFromWeb.get_chrome_path(self)
        self.UI()
        
        
    def UI(self):
        
        
        self.title("Sample Tkinter App")
        self.geometry("800x600")
        
        # Label for Text Input
        self.label = tk.Label(self, text="Website to fetch data: https://www.realestate.com.au")
        self.label.pack(pady=10)
        self.label = tk.Label(self, text=f"Chrome Path: {self.chrome_path}\nEDIT?")
        self.label.pack(pady=10)
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)
        
        # Yes, No buttons for Chrome path prompt
        self.yes_button = tk.Button(self.button_frame, text="Yes", command=self.prompt_for_chrome_path)
        self.yes_button.grid(row=0, column=0, padx=5, pady=5)
        self.no_button = tk.Button(self.button_frame, text="No", command=self.no_chrome_path)
        self.no_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Label for Table-like Structure with Checkboxes
        self.label_table = tk.Label(self, text="Select options:")
        self.label_table.pack(pady=10)
        
        # Dummy Data for Checkboxes
        self.options = [
            "House Name",
            "Property Attributes\n(Bedroom, Bathroom, Parking)",
            "Property Size",
            "Property Type\n(House, land, Town-house)",
            "Price",
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
            "Property Features": "property_features_item",
            "Loan Repay Amount(Estimate)": "loan_repay_item",
            "Description": "house_details",
            "Floor Plan(URL)": "floorplan_area",
            "Agent Name": "agent_name",
            "Agent Phone": "agent_phone",
            "Agent Organisation": "agent_org",
            "Agent Organisation Address": "agent_org_address"
        }
        
        # Create a frame to hold the checkboxes
        self.checkbox_frame = tk.Frame(self)
        self.checkbox_frame.pack(pady=10)
        
        # Variables to hold the state of checkboxes
        self.checkbox_vars = []
        
        # Create checkboxes in a 3-column grid with a cell skip pattern
        columns = 3
        for idx, option in enumerate(self.options):
            var = tk.BooleanVar()
            self.checkbox_vars.append(var)
            checkbox = tk.Checkbutton(self.checkbox_frame, text=option, variable=var, anchor='w', justify='left')
            row, col = divmod(idx, columns)
            col = col * 2  # Skip one cell each time
            checkbox.grid(row=row, column=col, padx=5, pady=5, sticky='w')
        
        # Create the "Select All" checkbox at the end, skipping 1 cell
        self.select_all_var = tk.BooleanVar()
        total_options = len(self.options)
        select_all_row, select_all_col = divmod(total_options, columns)
        select_all_col = select_all_col * 2  # Skip one cell
        self.select_all_checkbox = tk.Checkbutton(self.checkbox_frame, text="Select All", variable=self.select_all_var, command=self.select_all)
        self.select_all_checkbox.grid(row=select_all_row, column=select_all_col, padx=5, pady=5, sticky='w')
        
        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)
        while (len(GetDetailsFromWeb.get_chrome_path(self))) == 0:
            self.prompt_for_chrome_path()
    
    def prompt_for_chrome_path(self):
        # Prompt user to enter the Chrome path
        new_chrome_path = simpledialog.askstring("Input", "Please enter the Chrome path:")
        if new_chrome_path:
            self.chrome_path = new_chrome_path
            self.update_chrome_path()
            messagebox.showinfo("Info", "Chrome path updated successfully!")
            self.label.config(text=f"Chrome Path: {self.chrome_path}")
    def no_chrome_path(self):
        # Handle the case when the user clicks "No"
        messagebox.showinfo("Info", "Using existing Chrome path.")
    
    def update_chrome_path(self):
        # Update the chrome path in the config.json file
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
        # Set all checkboxes to the state of the "Select All" checkbox
        for var in self.checkbox_vars:
            var.set(self.select_all_var.get())
    
    def update_selection(self):
        # Get the selected items from the checkboxes
        selected_options = [self.option_names[self.options[idx]] for idx, var in enumerate(self.checkbox_vars) if var.get()]
        
        # Print the values to the console
        print(f"Selected Options: {selected_options}")
    
    def submit(self):
        # Get the selected items from the checkboxes
        selected_options = [self.option_names[self.options[idx]] for idx, var in enumerate(self.checkbox_vars) if var.get()]
        
        # Print the values to the console (or handle them as needed)
        # print(f"Selected Options: {selected_options}")
        GetDetailsFromWeb(selected_options)

# Run the application
if __name__ == "__main__":
    home_details=[]
    app = App()
    try:
        app.mainloop()
    except Exception as e:
        print("TK error here: ",e)