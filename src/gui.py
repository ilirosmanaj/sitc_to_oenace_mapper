import tkinter
from tkinter import *
import src.constants as const
from enum import Enum

# TODO: - add a label showing how many items are mapped already


def _format_sitc_item(key, value):
    return f'{key} - {value}'


def _get_code_from_text(text: str):
    if not text:
        return None

    return text.split('-')[0].strip()


EMPTY_CANDIDATES = {
    'text_similarity': [],
    'inverted_index': [],
}


class FiredFrom(Enum):
    OENACE = 'oenace'
    CANDIDATES = 'candidates'


class App:
    def __init__(self, sitc_codes, oeance_codes, oeance_candidates):
        self.sitc_codes = sitc_codes
        self.oeance_codes = oeance_codes
        self.oenace_candidates = oeance_candidates

        # store the sitc-oeance mappings here (sitc code is key, oeance code is value)
        self.mappings = {}

        self.root = tkinter.Tk()

        self.root.title = 'SITC to OENACE mapper'
        self.root.geometry(f'{const.WINDOW_WIDTH}x{const.WINDOW_HEIGHT}')

        self.sitc_listbox = Listbox(self.root, selectmode=SINGLE, bg=const.COLOR_ITEM_EMPTY)
        self.sitc_listbox.place(x=0, y=const.LISTBOX_DISTANCE_FROM_Y,
                                width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.sitc_listbox.bind("<Button>", self.sitc_list_selection)

        self.assign_scrollbar(self.sitc_listbox)
        self._fill_sitc_list()

        self.label_search = Label(self.root, text='Search SITC')
        self.label_search.place(x=0, y=0, width=120)

        self.sitc_search = Entry(self.root)
        self.sitc_search.place(x=150, y=0, width=150)
        self.sitc_search.bind("<Key>", self.on_sitc_search)

        self.sitc_candidates_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.sitc_candidates_listbox.place(x=const.LISTBOX_WIDTH + const.DISTANCE_BETWEEN_LISTBOXES, y=const.LISTBOX_DISTANCE_FROM_Y,
                                           width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.sitc_candidates_listbox.bind("<Double-Button>", self.candidates_doubleclick)

        self.assign_scrollbar(self.sitc_candidates_listbox)

        self.oenace_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.oenace_listbox.place(x=2*const.LISTBOX_WIDTH + 2 * const.DISTANCE_BETWEEN_LISTBOXES, y=const.LISTBOX_DISTANCE_FROM_Y,
                                  width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.oenace_listbox.bind("<Double-Button>", self.oenace_list_doubleclick)

        self.assign_scrollbar(self.oenace_listbox)

        self._fill_oeance_list()

        self.label_search = Label(self.root, text='Search OEANCE')
        self.label_search.place(x=500, y=0, width=120)

        self.oeance_search = Entry(self.root)
        self.oeance_search.place(x=600, y=0, width=150)
        self.oeance_search.bind("<Key>", self.on_oenace_search)

        self.current_mapping_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.current_mapping_listbox.place(x=0, y=2 * const.LISTBOX_DISTANCE_FROM_Y + const.LISTBOX_HEIGHT,
                                           width=const.MAPPING_LISTBOX_WIDTH,
                                           height=const.MAPPING_LISTBOX_HEIGHT)
        self.current_mapping_listbox.bind("<Button>", self.mapping_listbox_click)
        self.assign_scrollbar(self.current_mapping_listbox)

        self.btn_delete_mapping = Button(self.root, text='Delete Mapping', command=self.remove_mapping)
        self.btn_delete_mapping.place(x=1600, y=800, width=150)
        self.update_current_mappings()

        self.btn_save = Button(self.root, text='Save Mappings', command=self.save_mappings)
        self.btn_save.place(x=700, y=0, width=150)
        # self.btn_save.bind("<Key>", self.on_search)

    def remove_mapping(self, *args):
        current_selection = self.current_mapping_listbox.get(ACTIVE)
        current_sitc_code = current_selection.split('->')[0].split('-')[0].strip()
        self.mappings.pop(current_sitc_code)
        self.btn_delete_mapping.lower()

        self.update_current_mappings()
        self.update_sitc_selections()

    def mapping_listbox_click(self, *args):
        self.btn_delete_mapping.lift()
        print('Packing')

    @staticmethod
    def assign_scrollbar(listbox):
        scrollbar_x = Scrollbar(listbox, orient="horizontal")
        scrollbar_x.config(command=listbox.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        listbox.config(xscrollcommand=scrollbar_x.set)

        scrollbar_y = Scrollbar(listbox, orient="vertical")
        scrollbar_y.config(command=listbox.yview)
        scrollbar_y.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar_y.set)

    def save_mappings(self):
        print('Save button clicked')
        self.update_sitc_selections()

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
        # TODO (Ilir): this gets the last selected item, not the one that fired the event. Find a way to fix it
        selected_sitc = self.sitc_listbox.get(ACTIVE)

        # do not fill the list of candidates if nothing is selected
        if not selected_sitc:
            return

        selected_code = _get_code_from_text(selected_sitc)
        oenace_candidates = self.oenace_candidates.get(selected_code, EMPTY_CANDIDATES)
        all_candidates = oenace_candidates['text_similarity'] + oenace_candidates['inverted_index']

        self.sitc_candidates_listbox.delete(0, 'end')

        mapped_oenace_code = self.mappings.get(selected_code)
        i = 0
        for item in all_candidates:
            self.sitc_candidates_listbox.insert(i, _format_sitc_item(item['oenace_code'], item['oenace_title']))

            # if this sitc item has a mapping to an oenace code, highlight it
            if mapped_oenace_code == item['oenace_code']:
                self.sitc_candidates_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_MAPPED_CODE})
                self.sitc_candidates_listbox.yview_scroll(i, UNITS)

            i += 1

        # todo: if has a mapping, update the oenace listbox as well and scroll to that position
        if mapped_oenace_code:
            self.scroll_to_oenace_listbox_mapping(mapped_oenace_code)

    def scroll_to_oenace_listbox_mapping(self, oenace_code):
        i = 0
        for item in self.oenace_listbox.get(0, 'end'):
            item_code = _get_code_from_text(item)

            if item_code == oenace_code:
                self.oenace_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_MAPPED_CODE})
                self.oenace_listbox.yview_scroll(i, UNITS)
            else:
                self.oenace_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_EMPTY})

            i += 1

    def _fill_oeance_list(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items """
        self.oenace_listbox.delete(0, 'end')

        i = 0
        for oenace_code, oenace_title in self.oeance_codes.items():
            if not search_text:
                self.oenace_listbox.insert(i, _format_sitc_item(oenace_code, oenace_title))

            elif oenace_title.lower().startswith(search_text.lower()):
                self.oenace_listbox.insert(i, _format_sitc_item(oenace_code, oenace_title))

            i += 1

    def update_current_mappings(self):
        """Populates the listbox with corresponding sitc_items """
        self.current_mapping_listbox.delete(0, 'end')

        i = 0
        for sitc_code, oenace_code in self.mappings.items():
            sitc_item = self.sitc_codes.get(sitc_code)
            oenace_item = self.oeance_codes.get(oenace_code)
            formatted = f'{_format_sitc_item(sitc_code, sitc_item)} -> {_format_sitc_item(oenace_code, oenace_item)}'
            self.current_mapping_listbox.insert(i, formatted)
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

    def update_sitc_selections(self):
        """Go through sitc items and if it has a mapping, highlight it with grey on the listbox"""
        i = 0
        for item in self.sitc_listbox.get(0, 'end'):
            sitc_code = _get_code_from_text(item)

            if sitc_code in self.mappings.keys():
                self.sitc_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_HAS_SELECTION})
            else:
                self.sitc_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_EMPTY})
            i += 1

    def oenace_list_doubleclick(self, *args):
        self.assign_mapping_of_item(FiredFrom.OENACE)

    def candidates_doubleclick(self, *args):
        self.assign_mapping_of_item(FiredFrom.CANDIDATES)

    def assign_mapping_of_item(self, fired_from: FiredFrom):
        """Fired when candidates item or oenace item double clicked. Clicked item is chosen as the one for mapping"""
        # get the current selection from the sitc_item
        sitc_item = self.sitc_listbox.get(ACTIVE)

        # if no sitc item is currently selected, then do nothing (we do not know where to map it)
        if not sitc_item:
            print('No sitc item selected. Returning from mapping')
            return

        sitc_code = _get_code_from_text(sitc_item)

        if fired_from == FiredFrom.OENACE:
            oenace_item = self.oenace_listbox.get(ACTIVE)
            code = _get_code_from_text(oenace_item)
        else:
            oenace_candidate = self.sitc_candidates_listbox.get(ACTIVE)
            code = _get_code_from_text(oenace_candidate)

        if not code:
            print('Code empty, something was wrongly handled')
            return

        # update the current mappings
        self.mappings.update({
            sitc_code: code
        })
        self.update_current_mappings()
        self.update_sitc_selections()

    def start(self):
        self.root.mainloop()


def start_gui(sitc_codes, oeance_codes, oenace_candidates):
    app = App(sitc_codes=sitc_codes, oeance_codes=oeance_codes, oeance_candidates=oenace_candidates)
    app.start()