from tkinter.ttk import Treeview

class TreeViewUtils(Treeview):
    def __init__(self, parent, column_width = 100, **args):
        Treeview.__init__(self, parent, **args)

        self.pack(fill = 'both', expand = True)
        for column in self['columns']:
            self.column(column, width = column_width, anchor = 'center')
            self.heading(column, text = column,
                         )

    def config(self, item, value):
        self.config(item = item, value = value)

    def insert_data(self, values, parent = '', index = 'END', item = None):
        self.insert(parent, index, item, values = values)

    def sort_tree(self, tree, col, reverse, func):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key = func, reverse = reverse)
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command = lambda _col = col: self.sort_tree(tree, _col, not reverse, func))

    def delete_item(self, item):
        self.delete(item)

    def update_item(self, item, values):
        for i, value in enumerate(values):
            self.item(item, values = (value,))

    def search_item(self, values, index):
        for item in self.get_children():
            if self.item(item)["values"][index] == values:
                return item
        return None

    def bindEvent(self, event_name, func):
        self.bind(event_name, func)