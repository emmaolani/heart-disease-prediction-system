from tkinter import *
from tkinter import ttk
import pickle

model_file = 'db/settings.txt'


class Csv_gui:
    def __init__(self, root):
        self.combobox_val = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        self.cat_att = []
        self.cat_val = []

        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.hide_csv_gui)
        self.root.title('Settings')
        self.root.geometry('500x500+200+200')

        self.header_frame = Frame(self.root, padx=10, bg='lightgrey')
        self.header_frame.pack(fill=X, side=TOP)

        self.top_section_btn = Button(self.header_frame, text="position", bg="skyblue", border=0)
        self.top_section_btn.pack(side=RIGHT)

        self.bottom_section_btn = Button(self.header_frame, text="data type", bg="lightgreen", border=0)
        self.bottom_section_btn.pack(side=RIGHT, padx=6)

        self.frame = Frame(self.root, padx=10)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.top_section = LabelFrame(self.frame, text='Input position of attribute', padx=10)
        self.top_section.grid(row=0, column=0, sticky='nsew')
        self.__position_frame(self.top_section)

        self.age_name = Label(self.top_section, text='Age')
        self.age_name.grid(row=0, column=0, sticky='w')

        self.age_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.age_box.grid(row=1, column=0, sticky='nw')

        self.sex_name = Label(self.top_section, text='Sex')
        self.sex_name.grid(row=0, column=1, sticky='w')

        self.sex_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.sex_box.grid(row=1, column=1, sticky='nw')

        self.cp_name = Label(self.top_section, text='Cp')
        self.cp_name.grid(row=0, column=2, sticky='w')

        self.cp_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.cp_box.grid(row=1, column=2, sticky='nw')

        self.trest_name = Label(self.top_section, text='Trestbsp')
        self.trest_name.grid(row=0, column=3, sticky='w')

        self.trest_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.trest_box.grid(row=1, column=3, sticky='nw')

        self.chol_name = Label(self.top_section, text='Chol')
        self.chol_name.grid(row=0, column=4, sticky='w')

        self.chol_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.chol_box.grid(row=1, column=4, sticky='nw')

        self.fbs_name = Label(self.top_section, text='Fbs')
        self.fbs_name.grid(row=2, column=0, sticky='w')

        self.fbs_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.fbs_box.grid(row=3, column=0, sticky='nw')

        self.rest_name = Label(self.top_section, text='Restecg')
        self.rest_name.grid(row=2, column=1, sticky='w')

        self.rest_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.rest_box.grid(row=3, column=1, sticky='nw')

        self.thalch_name = Label(self.top_section, text='Thalch')
        self.thalch_name.grid(row=2, column=2, sticky='w')

        self.thalch_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.thalch_box.grid(row=3, column=2, sticky='nw')

        self.exang_name = Label(self.top_section, text='Exang')
        self.exang_name.grid(row=2, column=3, sticky='w')

        self.exang_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.exang_box.grid(row=3, column=3, sticky='nw')

        self.old_name = Label(self.top_section, text='Old peak')
        self.old_name.grid(row=2, column=4, sticky='w')

        self.old_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.old_box.grid(row=3, column=4, sticky='nw')

        self.slope_name = Label(self.top_section, text='Slope')
        self.slope_name.grid(row=4, column=0, sticky='w')

        self.slope_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.slope_box.grid(row=5, column=0, sticky='nw')

        self.ca_name = Label(self.top_section, text='Ca')
        self.ca_name.grid(row=4, column=1, sticky='w')

        self.ca_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.ca_box.grid(row=5, column=1, sticky='nw')

        self.thal_name = Label(self.top_section, text='Thal')
        self.thal_name.grid(row=4, column=2, sticky='w')

        self.thal_box = ttk.Combobox(self.top_section, values=self.combobox_val, width=33)
        self.thal_box.grid(row=5, column=2, sticky='nw')

        # bottom section *****************************************************
        self.bottom_section = LabelFrame(self.frame, text='Input position of attribute')
        self.bottom_section.grid(row=0, column=0, sticky='nsew')
        self.__position_frame(self.bottom_section)

        self.__create_bottom_section()

        self.hide_csv_gui()

    def __create_bottom_section(self):
        try:
            with open(model_file, 'rb') as file:
                data = pickle.load(file)
        except EOFError:
            att_pos = {"default_pos_name": ["Age", "Sex", "Cp", "Trestbsp", "Chol", "Fbs", "Restecg", "Thalch", "Exang","Oldpeak",
                                            "Slope", "Ca", "Thal", "num"],
                       "default_pos_val": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "new_pos_val": None
                       }

            category = {"default_cat_att": ["Sex", "Cp", "Restecg", "Exang", "Slope", "Ca", "Thal", "num"],
                        "default_catt_val": [["Male", "Female"],
                                              ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"],
                                              ["Normal", "ST-T", "Definite left"], ["Yes", "No"],
                                              ["upsloping", "flat", "downsloping"],
                                              ["color1", "color2", "color3", "color4"],
                                              ["Normal", "Fixed defect", "Reversible"],
                                              ["< 50% diameter narrowing", "> 50% diameter narrowing"]
                                              ],
                        "changed_cat_att": None,
                        "changed_cat_val": None,
                        "result": {"Sex": [1, 0], "Cp": [1, 2, 3, 4], "Restecg": [0, 1, 2], "Exang": [1, 0],
                                   "Slope": [1, 2, 3], "Ca": [0, 1, 2, 3], "Thal": [3, 6, 7], "Target": [0, 1]}
                        }
            data = [att_pos, category]
            with open(model_file, 'wb') as file:
                pickle.dump(data, file)

        row = 0
        column = 0

        for i in range(len(data[1]["default_cat_att"])):
            if i == 4:
                column = 0
                row = row + 2

            frame = Frame(self.bottom_section)
            frame.grid(row=row, column=column, sticky='nwes')
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            var = IntVar()
            c = Checkbutton(frame, variable=var, text=data[1]["default_cat_att"][i])
            c.grid(row=0, column=0, sticky="sw", padx=5)
            self.cat_att.append(var)

            column = column + 1

        row = 1
        column = 0

        for j in range(len(data[1]["default_catt_val"])):
            temp_cat_val = []
            if j == 4:
                column = 0
                row = row + 2

            frame = Frame(self.bottom_section)
            frame.grid(row=row, column=column, sticky='nwes')

            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)
            frame.rowconfigure(2, weight=1)
            frame.rowconfigure(3, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            for k in range(len(data[1]["default_catt_val"][j])):
                label = Label(frame, text="default (" + data[1]["default_catt_val"][j][k] + "): ")
                label.grid(row=k, column=0, sticky='w', padx=5)

                entry = Entry(frame, width=30)
                entry.grid(row=k, column=1, sticky='e', padx=5)

                temp_cat_val.append(entry)
            self.cat_val.append(temp_cat_val)

            column = column + 1

    @staticmethod
    def __position_frame(frame):
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

    def hide_csv_gui(self):
        self.root.withdraw()

    def show_csv_gui(self):
        self.root.deiconify()

#
# model_file = 'db/settings.txt'
#
# att_pos = {"default_pos_name": ["Age", "Sex", "Cp", "Trestbsp", "Chol", "Fbs", "Restecg", "Thalch", "Exang","Oldpeak",
#                                 "Slope", "Ca", "Thal", "num"],
#            "default_pos_val": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
#            "new_pos_val": None
#            }
#
# category = {"default_cat_att": ["Sex", "Cp", "Restecg", "Exang", "Slope", "Ca", "Thal", "num"],
#             "default_catt_val": [["Male", "Female"],
#                                   ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"],
#                                   ["Normal", "ST-T", "Definite left"], ["Yes", "No"],
#                                   ["upsloping", "flat", "downsloping"],
#                                   ["color1", "color2", "color3", "color4"],
#                                   ["Normal", "Fixed defect", "Reversible"],
#                                   ["< 50%", "> 50%"]
#                                   ],
#             "changed_cat_att": None,
#             "changed_cat_val": None,
#             "result": {"Sex": [1, 0], "Cp": [1, 2, 3, 4], "Restecg": [0, 1, 2], "Exang": [1, 0], "Slope": [1, 2, 3],
#                        "Ca": [0, 1, 2, 3], "Thal": [3, 6, 7], "Target": [0, 1]}
#             }
#
# with open(model_file, 'wb') as file:
#     pickle.dump([att_pos, category], file)
