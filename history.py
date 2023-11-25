from tkinter import *


class History:
    def __init__(self, root):
        self.root = root
        self.log_frames = []
        self.history_frame = Frame(self.root, width=300, background='lightgrey')
        self.history_frame.pack(fill=Y, side=RIGHT)
        self.history_frame.pack_propagate(0)
        self.history_header_frame = Frame(self.history_frame, background='lightgrey')
        self.history_header_frame.pack(fill=X)
        self.history_label = Label(self.history_header_frame,
                                   text='History',
                                   padx=7,
                                   pady=7,
                                   font=('sanserif', 9, 'bold'), background='lightgrey')
        self.history_label.pack(side=LEFT)

        self.history_close_btn = Button(self.history_header_frame,
                                        text='X',
                                        bg='lightgrey',
                                        font=('sanserif', 10),
                                        border=0)
        self.history_close_btn.pack(side=RIGHT, ipadx=2)
        self.log_frame = Frame(self.history_frame, background='lightgrey')
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.columnconfigure(1, weight=1)

        self.__create_logs()

        # self.scroll_btn_frame = Frame(self.history_frame, background='lightgrey')
        # self.scroll_btn_frame.pack(side=BOTTOM, fill=X)

        self.left_btn = Button(self.history_frame,
                               text='<',
                               font=('sanserif', 10),
                               border=0,
                               pady=5,
                               padx=5)
        self.left_btn.place(relx=0.01, rely=0.98, anchor='sw')

        self.right_btn = Button(self.history_frame,
                                text='>',
                                font=('sanserif', 10),
                                border=0,
                                pady=5,
                                padx=5)
        self.right_btn.place(relx=0.99, rely=0.98, anchor='se')

    def render(self,
               logs,
               log_index,
               show_widget, current_id, t_length, close_log, change_diagnosis, move_up, move_down, delete_data):

        self.history_close_btn.configure(command=close_log)
        self.left_btn.configure(command=move_up)
        self.right_btn.configure(command=move_down)
        index = log_index
        for i in range(10):
            if i < len(logs):
                self.log_frames[i]['log'].configure(text=logs[i])
                self.log_frames[i]['log'].configure(command=lambda sid=logs[i]: change_diagnosis(sid))
                self.log_frames[i]['del'].configure(text='del')
                self.log_frames[i]['del'].configure(command=lambda sid=logs[i]: delete_data(sid))
                if logs[i] == current_id:
                    self.log_frames[i]['log'].configure(background='grey')
                    self.log_frames[i]['del'].configure(background='grey')
                    self.log_frames[i]['log'].configure(fg='white')
                    self.log_frames[i]['del'].configure(fg='white')
                else:
                    self.log_frames[i]['log'].configure(background='lightgrey')
                    self.log_frames[i]['del'].configure(background='lightgrey')
                    self.log_frames[i]['log'].configure(fg='black')
                    self.log_frames[i]['del'].configure(fg='black')

            else:
                self.log_frames[i]['log'].configure(text='')
                self.log_frames[i]['del'].configure(text='')
                self.log_frames[i]['log'].configure(background='lightgrey')
                self.log_frames[i]['del'].configure(background='lightgrey')
                self.log_frames[i]['log'].configure(command="")
                self.log_frames[i]['del'].configure(command="")

            index = index + 1

        HMI = index / 10

        if index <= 10:
            self.left_btn.place_forget()
        else:
            self.left_btn.place(relx=0.01, rely=0.98, anchor='sw')

        if HMI > t_length or HMI == t_length:
            self.right_btn.place_forget()
        else:
            self.right_btn.place(relx=0.99, rely=0.98, anchor='se')

        if show_widget:
            self.history_frame.pack(fill=Y, side=RIGHT)
            self.history_frame.pack_propagate(0)
        else:
            self.history_frame.pack_forget()

    def __create_logs(self):
        for i in range(10):
            logs = Button(self.log_frame,
                          text='',
                          background='lightgrey',
                          width=37, border=0, font=('Times', 11), padx=5, pady=5)
            logs.grid(row=i, column=0, sticky='w')

            delete_btn = Button(self.log_frame,
                                text='',
                                background='lightgrey',
                                width=15, border=0, font=('Times', 11), padx=4, pady=5)
            delete_btn.grid(row=i, column=1)

            # pushing labels to an array to input values after loading diagnosis from db
            self.log_frames.append({})
            self.log_frames[i]['log'] = logs
            self.log_frames[i]['del'] = delete_btn

        self.log_frame.pack()
