import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import pandas as pd
import os


CSV_FILE = "crime_data.csv"


class CrimeLightingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime and Street Lighting App")

        self.records = []

        # Load existing CSV if available
        if os.path.exists(CSV_FILE):
            try:
                self.records = pd.read_csv(CSV_FILE).to_dict("records")
            except:
                pass

        # MODE SELECTION
        mode_frame = ttk.LabelFrame(root, text="Select Mode")
        mode_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.mode_var = tk.StringVar(value="manual")

        ttk.Radiobutton(mode_frame, text="Manual Input", variable=self.mode_var, value="manual",
                        command=self.switch_mode).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Radiobutton(mode_frame, text="Upload CSV/Excel", variable=self.mode_var, value="upload",
                        command=self.switch_mode).grid(row=0, column=1, sticky="w", padx=5)

        # MANUAL INPUT FRAME
        self.manual_frame = ttk.LabelFrame(root, text="Manual Entry")
        self.manual_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.manual_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(self.manual_frame, width=25)
        self.date_entry.grid(row=0, column=1)

        ttk.Label(self.manual_frame, text="Time (HH:MM, optional):").grid(row=1, column=0, sticky="w")
        self.time_entry = ttk.Entry(self.manual_frame, width=25)
        self.time_entry.grid(row=1, column=1)

        ttk.Label(self.manual_frame, text="Location:").grid(row=2, column=0, sticky="w")
        self.location_entry = ttk.Entry(self.manual_frame, width=25)
        self.location_entry.grid(row=2, column=1)

        ttk.Label(self.manual_frame, text="Crimes BEFORE lighting:").grid(row=3, column=0, sticky="w")
        self.before_entry = ttk.Entry(self.manual_frame, width=25)
        self.before_entry.grid(row=3, column=1)

        ttk.Label(self.manual_frame, text="Crimes AFTER lighting:").grid(row=4, column=0, sticky="w")
        self.after_entry = ttk.Entry(self.manual_frame, width=25)
        self.after_entry.grid(row=4, column=1)

        ttk.Button(self.manual_frame, text="Add Record", command=self.save_record).grid(row=5, column=0, pady=10)
        ttk.Button(self.manual_frame, text="Plot Last Record", command=self.plot_single).grid(row=5, column=1)
        ttk.Button(self.manual_frame, text="Plot Multi-Day/Location", command=self.plot_multi).grid(row=6, column=0, columnspan=2)
        ttk.Button(self.manual_frame, text="Save CSV", command=self.save_csv).grid(row=7, column=0, columnspan=2, pady=5)

        self.status_manual = ttk.Label(self.manual_frame, text="", foreground="green")
        self.status_manual.grid(row=8, column=0, columnspan=2, sticky="w")

        # UPLOAD MODE FRAME
        self.upload_frame = ttk.LabelFrame(root, text="Upload File")
        self.upload_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.upload_frame.grid_remove()

        ttk.Label(self.upload_frame, text="Your CSV/Excel must contain:").grid(row=0, column=0, sticky="w")
        ttk.Label(self.upload_frame, text="date, time(optional), location, before, after",
                  foreground="blue").grid(row=1, column=0, sticky="w")

        ttk.Button(self.upload_frame, text="Upload File", command=self.handle_file).grid(row=2, column=0, pady=10)

        self.status_upload = ttk.Label(self.upload_frame, text="", foreground="green")
        self.status_upload.grid(row=3, column=0, sticky="w")

    def switch_mode(self):
        mode = self.mode_var.get()
        if mode == "manual":
            self.manual_frame.grid()
            self.upload_frame.grid_remove()
        else:
            self.manual_frame.grid_remove()
            self.upload_frame.grid()

    def save_record(self):
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        location = self.location_entry.get().strip()
        before_str = self.before_entry.get().strip()
        after_str = self.after_entry.get().strip()

        if not date or not location or not before_str or not after_str:
            messagebox.showerror("Error", "Please fill date, location, and crime counts.")
            return

        try:
            before_val = int(before_str)
            after_val = int(after_str)
        except ValueError:
            messagebox.showerror("Error", "Crime counts must be integers.")
            return

        rec = {
            "date": date,
            "time": time,
            "location": location,
            "before": before_val,
            "after": after_val
        }

        self.records.append(rec)
        self.status_manual.config(text=f"Saved: {date} | {location}")

    def handle_file(self):
        path = filedialog.askopenfilename(
            title="Select CSV or Excel file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if not path:
            return

        try:
            df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        except:
            messagebox.showerror("Error", "Could not read file.")
            return

        required_cols = {"date", "location", "before", "after"}
        if not required_cols.issubset(set(df.columns)):
            messagebox.showerror("Error", "Missing required columns: date, location, before, after")
            return

        self.status_upload.config(text=f"Loaded {len(df)} records")

        self.plot_uploaded(df)

    def plot_uploaded(self, df):
        grouped = df.groupby(["date", "location"]).sum()[["before", "after"]].reset_index()

        plt.figure(figsize=(10, 5))
        x_labels = [f"{d}\n{loc}" for d, loc in zip(grouped["date"], grouped["location"])]
        x = range(len(grouped))

        plt.bar([i - 0.15 for i in x], grouped["before"], width=0.3, label="Before")
        plt.bar([i + 0.15 for i in x], grouped["after"], width=0.3, label="After")

        plt.xticks(x, x_labels, rotation=45, ha="right")
        plt.ylabel("Crimes")
        plt.title("Crime Comparison Across Dates/Locations")
        plt.legend()
        plt.tight_layout()
        plt.show()

        df["percent_reduction"] = ((df["before"] - df["after"]) / df["before"]) * 100

        plt.figure(figsize=(8, 5))
        plt.bar(df["location"], df["percent_reduction"])
        plt.title("Percent Reduction After Lighting")
        plt.ylabel("Reduction (%)")
        plt.tight_layout()
        plt.show()

    def plot_single(self):
        if not self.records:
            messagebox.showerror("Error", "No records available.")
            return

        rec = self.records[-1]
        labels = ["Before lighting", "After lighting"]
        values = [rec["before"], rec["after"]]

        plt.figure()
        plt.bar(labels, values)
        plt.title(f"{rec['date']} | {rec['location']}")
        plt.ylabel("Crimes")
        plt.tight_layout()
        plt.show()

    def plot_multi(self):
        if not self.records:
            messagebox.showerror("Error", "No data to plot.")
            return

        df = pd.DataFrame(self.records)
        grouped = df.groupby(["date", "location"]).sum()[["before", "after"]].reset_index()

        plt.figure(figsize=(10, 5))
        x_labels = [f"{d}\n{loc}" for d, loc in zip(grouped["date"], grouped["location"])]
        x = range(len(grouped))

        plt.bar([i - 0.15 for i in x], grouped["before"], width=0.3, label="Before")
        plt.bar([i + 0.15 for i in x], grouped["after"], width=0.3, label="After")

        plt.xticks(x, x_labels, rotation=45, ha="right")
        plt.ylabel("Crimes")
        plt.title("Crime Comparison Across Dates/Locations")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def save_csv(self):
        df = pd.DataFrame(self.records)
        df.to_csv(CSV_FILE, index=False)
        self.status_manual.config(text=f"Saved to {CSV_FILE}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CrimeLightingApp(root)
    root.mainloop()
