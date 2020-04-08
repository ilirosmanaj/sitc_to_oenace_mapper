import tkinter
from tkinter import *


class App:
    def __init__(self, sitc_codes, oeance_codes, oeance_candidates):
        self.sitc_codes = sitc_codes
        self.oeance_codes = oeance_codes
        self.oenace_candidates = oeance_candidates

        self.root = tkinter.Tk()

        self.root.title = 'SITC to OENACE mapper'
        self.root.geometry('800x800')

        self.sitc_listbox = Listbox(self.root)
        self.sitc_listbox.place(x=0, y=30, width=200, height=600)
        self._fill_sitc_list(sitc_codes)

        self.sitc_candidates_listbox = Listbox(self.root)
        self.sitc_candidates_listbox.place(x=250, y=30, width=200, height=600)
        self.sitc_candidates_listbox.bind("<Double-Button>", self.candidates_doubleclick)
        self._fill_sitc_candidates_list(sitc_codes)

        self.oeance_listbox = Listbox(self.root)
        self.oeance_listbox.place(x=500, y=30, width=200, height=600)
        self._fill_oeance_list(sitc_codes)

        self.label_search = Label(self.root, text='Search OEANCE')
        self.label_search.place(x=500, y=0, width=120)

        self.oeance_search = Entry(self.root)
        self.oeance_search.place(x=600, y=0, width=150)
        self.oeance_search.bind("<Key>", self.on_search)

        self.current_mapping = Listbox(self.root)
        self.current_mapping.place(x=20, y=700, width=750, height=250)
        self._fill_current_mappings(sitc_codes)

        self.btn_save = Button(self.root, text='Save Mappings', command=self.save_mappings)
        self.btn_save.place(x=700, y=0, width=150)
        self.btn_save.bind("<Key>", self.on_search)

        self.mappings = {}

        self.current = None

    def save_mappings(self):
        print('Save button clicked')
        self.sitc_candidates_listbox.itemconfig(1, {'bg': 'red'})
        self.oeance_listbox.itemconfig(5, {'bg': 'green'})
        pass

    def _fill_sitc_list(self, sitc_codes):
        """Populates the listbox with corresponding sitc_items """
        i = 1
        for j in range(1, 100):
            self.sitc_listbox.insert(i, f'SitcItem-{j}')
            i += 1
        # for sitc_code, sitc_title in sitc_codes.items():
        #     sitc_listbox.insert(i, f'{sitc_code} - {sitc_title}')
        #     i += 1

    def _fill_sitc_candidates_list(self, sitc_candidates):
        """Populates the listbox with corresponding sitc_items """
        i = 1
        for j in range(1, 10):
            self.sitc_candidates_listbox.insert(i, f'SitcCandidates-{j}')
            i += 1

    def _fill_oeance_list(self, oeance_codes):
        """Populates the listbox with corresponding sitc_items """
        i = 1
        for j in range(1, 10):
            self.oeance_listbox.insert(i, f'OEANCE-{j}')
            i += 1

    def _fill_current_mappings(self, oeance_codes):
        """Populates the listbox with corresponding sitc_items """
        i = 1
        for j in range(1, 10):
            self.oeance_listbox.insert(i, f'Mappings-{j}')
            i += 1

    def on_search(self, key):
        print(self.oeance_search.get())

    def candidates_doubleclick(self, *args):
        selection = self.sitc_candidates_listbox.selection_get()
        # we can do something with it
        print('Double click')

    def start(self):
        self.root.mainloop()


def start_gui():
    app = App(None, None, None)
    app.start()


# temporary shit
if __name__ == '__main__':
    start_gui()
