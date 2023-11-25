from tkinter import *
from inputField import InputField
from history import History


class MiddleSection:
    def __init__(self, root):
        self.root = root
        self.middle_frame = Frame(self.root, bg='#F5F5F5')
        self.middle_frame.place(relx=0.0, rely=0.1, relwidth=1, relheight=0.6)
        self.InputField = InputField(self.middle_frame)
        self.History = History(self.middle_frame)

    def render(self,
               state,
               logs, log_index, show_widget, sid, t_length, close_log, change_diagnosis, move_up, move_down, delete_data):

        self.InputField.render(state)
        self.History.render(logs,
                            log_index,
                            show_widget, sid, t_length, close_log, change_diagnosis, move_up, move_down, delete_data)
