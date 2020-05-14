import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from datetime import datetime

import gui.constants as const

from gui.classes import FiredFrom

from gui.csv_utils import CSVHandler
from gui.mapping_utils import CandidatesHandler
from gui.utils import format_sitc_item, get_code_from_text, get_sitc_code_from_mapping_text


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
        self.sitc_listbox.place(x=const.MARGIN_LEFT, y=const.LISTBOX_MARGIN_TOP,
                                width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.sitc_listbox.bind("<ButtonRelease-1>", self.sitc_list_selection)

        self._fill_sitc_list()

        self.sitc_search_label = Label(self.root, text='SITC items')
        self.sitc_search_label.place(x=const.MARGIN_LEFT, y=const.MARGIN_TOP, width=const.LABEL_WIDTH)

        self.sitc_search = Entry(self.root)
        self.sitc_search.place(x=const.MARGIN_LEFT + const.LABEL_WIDTH, y=const.MARGIN_TOP, width=const.ENTRY_WIDTH)
        self.sitc_search.bind("<KeyRelease>", self.on_sitc_search)

        self.sitc_info_label = Label(self.root, text='', font=("Helvetica", 10))
        self.sitc_info_label.place(x=const.MARGIN_LEFT + const.LABEL_WIDTH + const.ENTRY_WIDTH, y=const.MARGIN_TOP,
                                   width=const.LABEL_WIDTH)

        self.sitc_candidates_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.sitc_candidates_listbox.place(x=const.MARGIN_LEFT + const.LISTBOX_WIDTH + const.DISTANCE_BETWEEN_LISTBOXES,
                                           y=const.LISTBOX_MARGIN_TOP,
                                           width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.sitc_candidates_listbox.bind("<Double-Button-1>", self.candidates_doubleclick)
        self.sitc_candidates_listbox.bind("<ButtonRelease-1>", self.hide_delete_mapping_button)

        self.candidates_search_label = Label(self.root, text='Found Candidates')
        self.candidates_search_label.place(x=const.MARGIN_LEFT + const.LISTBOX_WIDTH + const.DISTANCE_BETWEEN_LISTBOXES,
                                           y=const.MARGIN_TOP,
                                           width=const.LABEL_WIDTH)

        self.candidates_dropdown = StringVar(self.root)

        choices = {'ALL', 'Fuzzy Matching', 'TF-IDF', 'Word Embedding'}
        self.candidates_dropdown.set('ALL')

        self.popupMenu = OptionMenu(self.root, self.candidates_dropdown, *choices)
        self.popupMenu.place(x=const.MARGIN_LEFT + const.LISTBOX_WIDTH + const.DISTANCE_BETWEEN_LISTBOXES +
                               const.LABEL_WIDTH + 20,
                             y=const.MARGIN_TOP - 5,
                             width=const.DROPDOWN_WIDTH)

        self.candidates_dropdown.trace('w', self.on_sitc_candidates_dropdown_change)

        self.oenace_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.oenace_listbox.place(x=const.MARGIN_LEFT + (2 * const.LISTBOX_WIDTH) + (2 * const.DISTANCE_BETWEEN_LISTBOXES),
                                  y=const.LISTBOX_MARGIN_TOP,
                                  width=const.LISTBOX_WIDTH, height=const.LISTBOX_HEIGHT)
        self.oenace_listbox.bind("<Double-Button-1>", self.oenace_list_doubleclick)
        self.oenace_listbox.bind("<ButtonRelease-1>", self.hide_delete_mapping_button)

        self._fill_oeance_list()

        self.oenace_search_label = Label(self.root, text='Search OEANCE')
        self.oenace_search_label.place(x=const.MARGIN_LEFT + (2*const.LISTBOX_WIDTH) +
                                         (2 * const.DISTANCE_BETWEEN_LISTBOXES),
                                       y=const.MARGIN_TOP, width=const.LABEL_WIDTH)

        self.oenace_search = Entry(self.root)
        self.oenace_search.place(x=const.MARGIN_LEFT + (2 * const.LISTBOX_WIDTH) + (2 * const.DISTANCE_BETWEEN_LISTBOXES)
                                   + const.LABEL_WIDTH,
                                 y=const.MARGIN_TOP, width=const.ENTRY_WIDTH)
        self.oenace_search.bind("<KeyRelease>", self.on_oenace_search)

        self.oenace_info_label = Label(self.root, text='', font=("Helvetica", 10))
        self.oenace_info_label.place(x=const.MARGIN_LEFT + (2*const.LISTBOX_WIDTH) + (2 * const.DISTANCE_BETWEEN_LISTBOXES)
                                        + const.LABEL_WIDTH + const.ENTRY_WIDTH, y=const.MARGIN_TOP,
                                   width=const.LABEL_WIDTH)

        self.current_mapping_listbox = Listbox(self.root, bg=const.COLOR_ITEM_EMPTY)
        self.current_mapping_listbox.place(x=const.MARGIN_LEFT,
                                           y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT +
                                             const.MAPPING_LISTBOX_MARGIN_TOP,
                                           width=const.MAPPING_LISTBOX_WIDTH,
                                           height=const.MAPPING_LISTBOX_HEIGHT)
        self.current_mapping_listbox.bind("<ButtonRelease-1>", self.mapping_listbox_click)

        self.mapping_search_label = Label(self.root, text='Mapped items')
        self.mapping_search_label.place(x=const.MARGIN_LEFT,
                                        y=const.MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP,
                                        width=const.LABEL_WIDTH)

        self.mapping_search = Entry(self.root)
        self.mapping_search.place(
            x=const.MARGIN_LEFT + const.LABEL_WIDTH,
            y=const.MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP,
            width=const.ENTRY_WIDTH
        )
        self.mapping_search.bind("<KeyRelease>", self.on_mapping_search)

        self.currently_mapped_info_label = Label(self.root, text='')
        self.currently_mapped_info_label.place(
            x=const.MARGIN_LEFT + (const.MAPPING_LISTBOX_WIDTH/2) - (const.LABEL_WIDTH / 2),
            y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP -
              const.MAPPING_LISTBOX_ITEMS_ON_TOP,
            width=const.LABEL_WIDTH
        )

        self.btn_delete_mapping = Button(self.root, text='Delete Mapping', command=self.remove_mapping)
        self.btn_delete_mapping.place(
            x=const.MARGIN_LEFT + const.MAPPING_LISTBOX_WIDTH - const.BUTTON_WIDTH,
            y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP -
              const.MAPPING_LISTBOX_ITEMS_ON_TOP,
            width=const.BUTTON_WIDTH,
            height=30,
        )

        self.lbl_ghost = Label(self.root, text=' ' * 14)
        self.lbl_ghost.place(
            x=const.MARGIN_LEFT + const.MAPPING_LISTBOX_WIDTH - const.BUTTON_WIDTH,
            y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP -
              const.MAPPING_LISTBOX_ITEMS_ON_TOP,
            width=const.BUTTON_WIDTH,
            height=30
        )
        self.lbl_ghost.lift()

        self.fill_current_mappings_listbox()

        self.assign_scrollbars_to_listboxes()

        self.btn_save = Button(self.root, text='Save Mappings', command=self.save_mappings)
        self.btn_save.place(x=const.MARGIN_LEFT + const .MAPPING_LISTBOX_WIDTH - const.BUTTON_WIDTH,
                            y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP +
                              const.MAPPING_LISTBOX_HEIGHT,
                            width=const.BUTTON_WIDTH)

        self.btn_load_from_file = Button(self.root, text='Load Mapping', command=self.load_mappings)
        self.btn_load_from_file.place(
            x=const.MARGIN_LEFT + const .MAPPING_LISTBOX_WIDTH - (2 * const.BUTTON_WIDTH),
            y=const.LISTBOX_MARGIN_TOP + const.LISTBOX_HEIGHT + const.MAPPING_LISTBOX_MARGIN_TOP +
              const.MAPPING_LISTBOX_HEIGHT,
            width=const.BUTTON_WIDTH
        )

        self.csv_handler = CSVHandler()
        self.candidates_handler = CandidatesHandler()

    def update_sitc_items_shown(self):
        sitc_total = len(self.sitc_codes)
        showing = self.sitc_listbox.size()
        self.sitc_info_label['text'] = f'Showing {showing}/{sitc_total}'

    def update_oenace_items_shown(self):
        oenace_total = len(self.oeance_codes)
        showing = self.oenace_listbox.size()
        self.oenace_info_label['text'] = f'Showing {showing}/{oenace_total}'

    def update_mapped_items_counts(self):
        sitc_total = len(self.sitc_codes)
        mapped = len(self.mappings)
        self.currently_mapped_info_label['text'] = f'Mapped {mapped}/{sitc_total}'

    def hide_delete_mapping_button(self, *args):
        self.btn_delete_mapping.lower()
        self.lbl_ghost.lift()

    def on_sitc_candidates_dropdown_change(self, *args):
        sitc_item = self.sitc_listbox.get(ACTIVE)

        # if no sitc item is currently selected, then do nothing (we do not know where to map it)
        if not sitc_item:
            print('No sitc item selected. Returning from mapping')
            return

        sitc_code = get_code_from_text(sitc_item)

        self.update_candidates_list(sitc_code)

    def remove_mapping(self, *args):
        current_selection = self.current_mapping_listbox.get(ACTIVE)
        current_sitc_code = current_selection.split('->')[0].split('-')[0].strip()
        self.mappings.pop(current_sitc_code)

        self.hide_delete_mapping_button()
        self.fill_current_mappings_listbox()
        self.update_sitc_selections()

    def load_mappings(self, *args):
        Tk().withdraw()
        filename = askopenfilename()

        if not filename:
            print('No file selected, returning')
            return

        self.mappings = self.csv_handler.load_results(filename)
        self.oenace_candidates = self.candidates_handler.load_candidates(filename)

        self.fill_current_mappings_listbox()
        self.update_sitc_selections()

    def mapping_listbox_click(self, *args):
        self.btn_delete_mapping.lift()
        self.lbl_ghost.lower()

    def assign_scrollbars_to_listboxes(self):
        for listbox in [self.sitc_listbox, self.sitc_candidates_listbox, self.oenace_listbox,
                        self.current_mapping_listbox]:
            scrollbar_x = Scrollbar(listbox, orient="horizontal")
            scrollbar_x.config(command=listbox.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            listbox.config(xscrollcommand=scrollbar_x.set)

            scrollbar_y = Scrollbar(listbox, orient="vertical")
            scrollbar_y.config(command=listbox.yview)
            scrollbar_y.pack(side="right", fill="y")
            listbox.config(yscrollcommand=scrollbar_y.set)

    def save_mappings(self):
        file_name = f'mapping-{datetime.now().isoformat()}'

        stored_at = self.csv_handler.store_results(self.mappings, file_name)
        self.candidates_handler.store_candidates(self.oenace_candidates, file_name)

        messagebox.showinfo(title='Mapping successfully saved', message=f'We have saved your mapping in '
                                                                        f'location {stored_at}')

    def _fill_sitc_list(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items"""
        i = 0
        self.sitc_listbox.delete(0, 'end')

        if search_text:
            search_text = search_text.lower()

        for sitc_code, sitc_title in self.sitc_codes.items():
            if not search_text:
                self.sitc_listbox.insert(i, format_sitc_item(sitc_code, sitc_title))

            elif search_text in sitc_title.lower() or search_text in sitc_code.lower():
                self.sitc_listbox.insert(i, format_sitc_item(sitc_code, sitc_title))
            i += 1

    def update_candidates_list(self, selected_code):
        """Populates the listbox with corresponding sitc_items """
        oenace_candidates = self.oenace_candidates.get(selected_code, const.EMPTY_CANDIDATES)
        method = self.candidates_dropdown.get()

        PICK_AT_MOST_FROM_METHOD = 8

        if method == 'ALL':
            all_candidates = oenace_candidates['text_similarity'][:3] \
                             + oenace_candidates['inverted_index'][:3] \
                             + oenace_candidates['word_embedding'][:5]

        elif method == 'Fuzzy Matching':
            all_candidates = oenace_candidates['text_similarity'][:PICK_AT_MOST_FROM_METHOD]

        elif method == 'TF-IDF':
            all_candidates = oenace_candidates['inverted_index'][:PICK_AT_MOST_FROM_METHOD]

        else:
            all_candidates = oenace_candidates['word_embedding'][:PICK_AT_MOST_FROM_METHOD]

        # convert to set to remove duplicates
        items = set([(oenace_item['oenace_code'], oenace_item['oenace_title']) for oenace_item in all_candidates])

        self.sitc_candidates_listbox.delete(0, 'end')

        mapped_oenace_code = self.mappings.get(selected_code)
        i = 0
        for oenace_code, oenace_title in items:
            self.sitc_candidates_listbox.insert(i, format_sitc_item(oenace_code, oenace_title))

            # if this sitc item has a mapping to an oenace code, highlight it
            if mapped_oenace_code == oenace_code:
                self.sitc_candidates_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_MAPPED_CODE})
                self.sitc_candidates_listbox.see(i)
            else:
                self.sitc_candidates_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_EMPTY})

            i += 1

        self.scroll_to_oenace_listbox_mapping(mapped_oenace_code)

    def scroll_to_oenace_listbox_mapping(self, oenace_code):
        i = 0
        for item in self.oenace_listbox.get(0, 'end'):
            item_code = get_code_from_text(item)

            if item_code == oenace_code:
                self.oenace_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_MAPPED_CODE})
                self.oenace_listbox.see(i)
            else:
                self.oenace_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_EMPTY})

            i += 1

    def update_mapping_listbox(self, sitc_code):
        i = 0
        for item in self.current_mapping_listbox.get(0, 'end'):
            code = get_sitc_code_from_mapping_text(item)

            if sitc_code == code:
                self.current_mapping_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_MAPPED_CODE})
                self.current_mapping_listbox.see(i)
            else:
                self.current_mapping_listbox.itemconfig(i, {'bg': const.COLOR_ITEM_EMPTY})

            i += 1

    def _fill_oeance_list(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items """
        self.oenace_listbox.delete(0, 'end')

        if search_text:
            search_text = search_text.lower()

        i = 0
        for oenace_code, oenace_title in self.oeance_codes.items():
            if not search_text:
                self.oenace_listbox.insert(i, format_sitc_item(oenace_code, oenace_title))

            elif search_text in oenace_code.lower() or search_text in oenace_title.lower():
                self.oenace_listbox.insert(i, format_sitc_item(oenace_code, oenace_title))

            i += 1

    def fill_current_mappings_listbox(self, search_text: str = None):
        """Populates the listbox with corresponding sitc_items """
        self.current_mapping_listbox.delete(0, 'end')

        i = 0
        for sitc_code, oenace_code in self.mappings.items():
            sitc_item = self.sitc_codes.get(sitc_code)
            oenace_item = self.oeance_codes.get(oenace_code)
            formatted = f'{format_sitc_item(sitc_code, sitc_item)} -> {format_sitc_item(oenace_code, oenace_item)}'

            if not search_text:
                self.current_mapping_listbox.insert(i, formatted)
            elif search_text in formatted:
                self.current_mapping_listbox.insert(i, formatted)

            i += 1

        # scroll to the end
        self.current_mapping_listbox.see(i)

        self.update_mapped_items_counts()

    def on_mapping_search(self, key):
        self.fill_current_mappings_listbox(self.mapping_search.get())

    def on_sitc_search(self, key):
        self._fill_sitc_list(self.sitc_search.get())
        self.update_sitc_items_shown()
        self.update_sitc_selections()

    def on_oenace_search(self, key):
        self._fill_oeance_list(self.oenace_search.get())
        self.update_oenace_items_shown()

    def clear_oenace_searches(self):
        self.oenace_search.delete(0, 'end')
        self._fill_oeance_list()
        self.update_oenace_items_shown()

    def sitc_list_selection(self, *args):
        """
        Handle selection of an item in sitc list.
        If the selected item has already a chosen mapping, preselect it. If not, do nothing
        """
        # on item selection, check if oenace searchbox has already some filters. If yes delete them
        if self.oenace_search.get():
            self.clear_oenace_searches()
        # hide button if shown
        self.hide_delete_mapping_button()


        index = self.sitc_listbox.curselection()[0]
        selected_sitc = self.sitc_listbox.get(index)

        sitc_code = get_code_from_text(selected_sitc)

        self.update_candidates_list(sitc_code)
        self.update_mapping_listbox(sitc_code)

    def update_sitc_selections(self):
        """Go through sitc items and if it has a mapping, highlight it with grey on the listbox"""
        i = 0
        for item in self.sitc_listbox.get(0, 'end'):
            sitc_code = get_code_from_text(item)

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

        sitc_code = get_code_from_text(sitc_item)

        if fired_from == FiredFrom.OENACE:
            oenace_item = self.oenace_listbox.get(ACTIVE)
            code = get_code_from_text(oenace_item)
        else:
            oenace_candidate = self.sitc_candidates_listbox.get(ACTIVE)
            code = get_code_from_text(oenace_candidate)

        if not code:
            print('Code empty, something was wrongly handled')
            return

        # update the current mappings
        self.mappings.update({
            sitc_code: code
        })
        self.fill_current_mappings_listbox()
        self.update_sitc_selections()

    def start(self):
        self.root.mainloop()


def start_gui(sitc_codes, oeance_codes, oenace_candidates):
    app = App(sitc_codes=sitc_codes, oeance_codes=oeance_codes, oeance_candidates=oenace_candidates)
    app.start()
