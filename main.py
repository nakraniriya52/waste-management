import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import add_record
from analysis import get_summary, filter_records, high_waste_areas
from charts import show_category_chart, show_location_chart, show_time_graph

BG = '#F4F7FB'
NAVY = '#17324D'
ACCENT = '#2F6F6D'
ACCENT_DARK = '#245958'
MUTED = '#6B7A7A'
BORDER = '#D9E1E1'
WHITE = '#FFFFFF'
TEXT = '#263238'

class WasteApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Waste Collection Management System')
        self.root.geometry('1100x760')
        self.root.minsize(950, 680)
        self.root.configure(bg=BG)

        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            pass
        self.style.configure('TLabel', background=BG, foreground=TEXT, font=('Segoe UI', 10))
        self.style.configure('TLabelframe', background=BG, bordercolor=BORDER, relief='solid', borderwidth=1)
        self.style.configure('TLabelframe.Label', background=BG, foreground=NAVY,
                             font=('Segoe UI', 11, 'bold'))
        self.style.configure('Treeview', rowheight=30, font=('Segoe UI', 10),
                             background=WHITE, fieldbackground=WHITE, foreground=TEXT)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                             background=NAVY, foreground=WHITE, padding=8)
        self.style.map('Treeview', background=[('selected', '#DCEBFF')],
                       foreground=[('selected', NAVY)])
        self.style.configure('TEntry', padding=7)

        self.build_header()
        self.build_summary_cards()
        self.build_form()
        self.build_search()
        self.build_chart_buttons()
        self.build_table()
        self.refresh()

    def make_button(self, parent, text, command, width=16, primary=False):
        bg = ACCENT if primary else WHITE
        fg = WHITE if primary else NAVY
        active = ACCENT_DARK if primary else '#EEF3F3'
        b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                      activebackground=active, activeforeground=fg,
                      font=('Segoe UI', 9, 'bold'), relief='solid', bd=1,
                      highlightthickness=0, padx=11, pady=7, cursor='hand2', width=width)
        return b

    def build_header(self):
        header = tk.Frame(self.root, bg=NAVY, height=112)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='♻', bg=NAVY, fg='#7DE2A7',
                 font=('Segoe UI Symbol', 32, 'bold')).pack(pady=(10, 0))
        tk.Label(header, text='WASTE COLLECTION MANAGEMENT SYSTEM',
                 bg=NAVY, fg=WHITE, font=('Segoe UI', 20, 'bold')).pack()
        tk.Label(header, text='Record • Analyze • Compare • Plan',
                 bg=NAVY, fg='#C9D8E8', font=('Segoe UI', 10)).pack(pady=(1, 8))

    def build_summary_cards(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill='x', padx=22, pady=(12, 4))

        # Three simple dashboard cards keep the important results visible.
        cards = []
        for i in range(3):
            card = tk.Frame(frame, bg=WHITE, highlightbackground=BORDER,
                            highlightthickness=1, padx=14, pady=9)
            card.pack(side='left', fill='x', expand=True,
                      padx=(0 if i == 0 else 5, 5 if i < 3 else 0))
            cards.append(card)

        self.total_card, self.average_card, self.records_card = cards

        tk.Label(self.total_card, text='TOTAL WASTE',
                 bg=WHITE, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.total_value = tk.Label(self.total_card, text='0.00 kg',
                                    bg=WHITE, fg=ACCENT,
                                    font=('Segoe UI', 18, 'bold'))
        self.total_value.pack(anchor='w', pady=(3, 0))

        tk.Label(self.average_card, text='AVERAGE WASTE PER RECORD',
                 bg=WHITE, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.average_value = tk.Label(self.average_card, text='0.00 kg',
                                      bg=WHITE, fg=ACCENT,
                                      font=('Segoe UI', 18, 'bold'))
        self.average_value.pack(anchor='w', pady=(3, 0))

        tk.Label(self.records_card, text='TOTAL RECORDS',
                 bg=WHITE, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.records_value = tk.Label(self.records_card, text='0',
                                      bg=WHITE, fg=ACCENT,
                                      font=('Segoe UI', 18, 'bold'))
        self.records_value.pack(anchor='w', pady=(3, 0))

    def build_form(self):
        frame = ttk.LabelFrame(self.root, text='  Add New Waste Record  ', padding=12)
        frame.pack(fill='x', padx=22, pady=(15, 8))
        labels = ['Date (YYYY-MM-DD)', 'Location', 'Category', 'Quantity (kg)']
        self.date_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        variables = [self.date_var, self.location_var, self.category_var, self.qty_var]
        for i, (label, var) in enumerate(zip(labels, variables)):
            ttk.Label(frame, text=label).grid(row=0, column=i, sticky='w', padx=7, pady=(0, 4))
            ttk.Entry(frame, textvariable=var, width=22).grid(row=1, column=i, padx=7, sticky='ew')
        self.make_button(frame, '＋ Add Record', self.add, 15, primary=True).grid(row=1, column=4, padx=8, pady=8)
        for i in range(4):
            frame.columnconfigure(i, weight=1)

    def build_search(self):
        frame = ttk.LabelFrame(self.root, text='  Search & Analysis  ', padding=10)
        frame.pack(fill='x', padx=22, pady=8)
        self.search_var = tk.StringVar()
        ttk.Label(frame, text='Search by date, location or category:').pack(side='left', padx=(5, 7))
        entry = ttk.Entry(frame, textvariable=self.search_var, width=28)
        entry.pack(side='left', padx=5)
        entry.bind('<Return>', lambda event: self.refresh())
        self.make_button(frame, '🔎 Search / Filter', self.refresh, 15, primary=True).pack(side='left', padx=5, pady=3)
        self.make_button(frame, '↻ Show All', self.show_all, 12).pack(side='left', padx=5, pady=3)
        self.make_button(frame, 'Σ Summary', self.summary, 12).pack(side='left', padx=5, pady=3)
        self.make_button(frame, '⚠ High-Waste Areas', self.high_areas, 17).pack(side='left', padx=5, pady=3)

    def build_chart_buttons(self):
        frame = ttk.LabelFrame(self.root, text='  Visual Reports  ', padding=8)
        frame.pack(fill='x', padx=22, pady=8)
        self.make_button(frame, '📊 Category Bar Chart', show_category_chart, 20, primary=True).pack(side='left', padx=5, pady=3)
        self.make_button(frame, '📊 Location Bar Chart', show_location_chart, 20).pack(side='left', padx=5, pady=3)
        self.make_button(frame, '📈 Waste Over Time', show_time_graph, 20).pack(side='left', padx=5, pady=3)

    def build_table(self):
        frame = ttk.LabelFrame(self.root, text='  Waste Records  ', padding=8)
        frame.pack(fill='both', expand=True, padx=22, pady=(8, 18))
        table_frame = tk.Frame(frame, bg=WHITE)
        table_frame.pack(fill='both', expand=True)
        cols = ('date', 'location', 'category', 'quantity')
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        headings = {'date': 'Date', 'location': 'Location', 'category': 'Category', 'quantity': 'Quantity (kg)'}
        widths = {'date': 170, 'location': 230, 'category': 230, 'quantity': 180}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c], anchor='center')
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.status = tk.Label(frame, text='Ready', bg=BG, fg=MUTED,
                               font=('Segoe UI', 9), anchor='w')
        self.status.pack(fill='x', pady=(6, 0))

    def add(self):
        try:
            add_record(self.date_var.get().strip(), self.location_var.get().strip(),
                       self.category_var.get().strip(), self.qty_var.get().strip())
            messagebox.showinfo('Record Added', 'Waste record was added successfully.')
            for var in [self.date_var, self.location_var, self.category_var, self.qty_var]:
                var.set('')
            self.refresh()
        except ValueError as e:
            messagebox.showerror('Invalid Input', str(e))
        except Exception as e:
            messagebox.showerror('Error', f'Could not save record:\n{e}')

    def refresh(self):
        rows = filter_records(self.search_var.get().strip())
        self.fill_table(rows)

        # Keep the dashboard values visible and update them after every change/search.
        if rows:
            total = sum(float(r['quantity']) for r in rows)
            average = total / len(rows)
        else:
            total = 0
            average = 0

        self.total_value.config(text=f'{total:.2f} kg')
        self.average_value.config(text=f'{average:.2f} kg')
        self.records_value.config(text=str(len(rows)))

        self.status.config(text=f'{len(rows)} record(s) displayed')

    def show_all(self):
        self.search_var.set('')
        self.refresh()

    def fill_table(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['date'], r['location'], r['category'], f"{r['quantity']:.2f}"))

    def summary(self):
        try:
            s = get_summary()
            messagebox.showinfo(
                'Waste Summary',
                f"TOTAL WASTE\n{s['total']:.2f} kg\n\n"
                f"AVERAGE PER RECORD\n{s['average']:.2f} kg\n\n"
                f"NUMBER OF RECORDS\n{s['count']}"
            )
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def high_areas(self):
        areas = high_waste_areas()
        if not areas:
            messagebox.showinfo('High-Waste Areas', 'No records available.')
            return
        text = '\n'.join(f'{i + 1}. {loc} — {qty:.2f} kg' for i, (loc, qty) in enumerate(areas))
        messagebox.showinfo('High-Waste Areas', text)

if __name__ == '__main__':
    root = tk.Tk()
    WasteApp(root)
    root.mainloop()
