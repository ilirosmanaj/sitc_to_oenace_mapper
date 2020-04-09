import tkinter
from tkinter import *


def _format_sitc_item(key, value):
    return f'{key} - {value}'


def _get_code_from_text(text: str):
    return text.split('-')[0].strip()


EMPTY_CANDIDATES = {
    'text_similarity': [],
    'inverted_index': [],
}


class App:
    def __init__(self, sitc_codes, oeance_codes, oeance_candidates):
        self.sitc_codes = sitc_codes
        self.oeance_codes = oeance_codes
        self.oenace_candidates = oeance_candidates

        # store the sitc-oeance mappings here (sitc code is key, oeance code is value)
        self.mappings = {}

        self.root = tkinter.Tk()

        self.root.title = 'SITC to OENACE mapper'
        self.root.geometry('1200x1000')

        self.sitc_listbox = Listbox(self.root)
        self.sitc_listbox.place(x=0, y=30, width=200, height=600)
        self.sitc_listbox.bind("<Button>", self.sitc_list_selection)

        scrollbar = self.assign_scrollbar(self.sitc_listbox)
        self.sitc_listbox.config(yscrollcommand=scrollbar.set)
        self._fill_sitc_list()

        self.label_search = Label(self.root, text='Search SITC')
        self.label_search.place(x=0, y=0, width=120)

        self.sitc_search = Entry(self.root)
        self.sitc_search.place(x=150, y=0, width=150)
        self.sitc_search.bind("<Key>", self.on_sitc_search)

        self.sitc_candidates_listbox = Listbox(self.root)
        self.sitc_candidates_listbox.place(x=250, y=30, width=200, height=600)
        self.sitc_candidates_listbox.bind("<Button>", self.candidates_click)
        self.sitc_candidates_listbox.bind("<Double-Button>", self.candidates_doubleclick)

        scrollbar = self.assign_scrollbar(self.sitc_candidates_listbox)
        self.sitc_candidates_listbox.config(yscrollcommand=scrollbar.set)

        self.oeance_listbox = Listbox(self.root)
        self.oeance_listbox.place(x=500, y=30, width=200, height=600)
        self.oeance_listbox.bind("<Double-Button>", self.oenace_list_doubleclick)

        scrollbar = self.assign_scrollbar(self.oeance_listbox)
        self.oeance_listbox.config(yscrollcommand=scrollbar.set)

        self._fill_oeance_list()

        self.label_search = Label(self.root, text='Search OEANCE')
        self.label_search.place(x=500, y=0, width=120)

        self.oeance_search = Entry(self.root)
        self.oeance_search.place(x=600, y=0, width=150)
        self.oeance_search.bind("<Key>", self.on_oenace_search)

        self.current_mapping_listbox = Listbox(self.root)
        self.current_mapping_listbox.place(x=20, y=700, width=750, height=250)

        scrollbar = self.assign_scrollbar(self.current_mapping_listbox)
        self.current_mapping_listbox.config(yscrollcommand=scrollbar.set)

        self.update_current_mappings()

        self.btn_save = Button(self.root, text='Save Mappings', command=self.save_mappings)
        self.btn_save.place(x=700, y=0, width=150)
        # self.btn_save.bind("<Key>", self.on_search)

    @staticmethod
    def assign_scrollbar(listbox):
        scrollbar = Scrollbar(listbox, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        return scrollbar

    def save_mappings(self):
        print('Save button clicked')
        self.update_sitc_selections()
        pass

    def _fill_sitc_list(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items"""
        i = 0
        self.sitc_listbox.delete(0, 'end')

        for sitc_code, sitc_title in self.sitc_codes.items():
            if not search_text:
                self.sitc_listbox.insert(i, _format_sitc_item(sitc_code, sitc_title))

            elif sitc_title.lower().startswith(search_text.lower()):
                self.sitc_listbox.insert(i, _format_sitc_item(sitc_code, sitc_title))
            i += 1

    def update_candidates_list(self):
        """Populates the listbox with corresponding sitc_items """
        selected_sitc = self.sitc_listbox.get(ACTIVE)

        # do not fill the list of candidates if nothing is selected
        if not selected_sitc:
            return

        selected_code = _get_code_from_text(selected_sitc)
        oenace_candidates = self.oenace_candidates.get(selected_code, EMPTY_CANDIDATES)
        all_candidates = oenace_candidates['text_similarity'] + oenace_candidates['inverted_index']

        self.sitc_candidates_listbox.delete(0, 'end')

        i = 0
        for item in all_candidates:
            self.sitc_candidates_listbox.insert(i, _format_sitc_item(item['oenace_code'], item['oenace_title']))
            i += 1
        self.sitc_candidates_listbox.update()
        print('Updated the candidates list')

    def _fill_oeance_list(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items """
        self.oeance_listbox.delete(0, 'end')

        i = 0
        for oenace_code, oenace_title in self.oeance_codes.items():
            if not search_text:
                self.oeance_listbox.insert(i, _format_sitc_item(oenace_code, oenace_title))

            elif oenace_title.lower().startswith(search_text.lower()):
                self.oeance_listbox.insert(i, _format_sitc_item(oenace_code, oenace_title))

            i += 1

    def update_current_mappings(self):
        """Populates the listbox with corresponding sitc_items """
        self.mappings.update({
            'iliri': 'baba',
            'donika': 'hudhra, qepa'
        })

        i = 0
        for sitc_code, oeance_code in self.mappings.items():
            self.current_mapping_listbox.insert(i, _format_sitc_item(sitc_code, oeance_code))
            i += 1

    def on_sitc_search(self, key):
        self._fill_sitc_list(self.sitc_search.get())

    def on_oenace_search(self, key):
        self._fill_oeance_list(self.oeance_search.get())

    def sitc_list_selection(self, *args):
        """
        Handle selection of an item in sitc list.
        If the selected item has already a chosen mapping, preselect it. If not, do nothing
        """
        self.update_candidates_list()

        # consider
        # print('Button click on the sitc list')

    def update_sitc_selections(self):
        """Go through sitc items and if it has a mapping, highlight it with grey on the listbox"""
        i = 0
        for item in self.sitc_listbox.get(0, 'end'):
            sitc_code = _get_code_from_text(item)

            if sitc_code in self.mappings.keys():
                self.oeance_listbox.itemconfig(i, {'bg': 'grey'})
            i += 1

    def oenace_list_doubleclick(self, *args):
        selection = self.sitc_candidates_listbox.selection_get()
        # we can do something with it
        print('Double click on the oeance list')

    def candidates_click(self, *args):
        selection = self.sitc_candidates_listbox.selection_get()
        # we can do something with it
        print('click on the candidates')

    def candidates_doubleclick(self, *args):
        selection = self.sitc_candidates_listbox.selection_get()
        # we can do something with it
        print('Double click on the candidates')

    def start(self):
        self.root.mainloop()


def start_gui(sitc_codes, oeance_codes, oenace_candidates):
    app = App(sitc_codes=sitc_codes, oeance_codes=oeance_codes, oeance_candidates=oenace_candidates)
    app.start()
