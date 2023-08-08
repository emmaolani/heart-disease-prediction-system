from tkinter import *
from tkinter import filedialog
from main import main_pro

root = Tk()
root.title('heart disease prediction system')
width = root.winfo_screenwidth()
print(width)


def browse_file():
    main_frame = Frame(root, width=1080, height=1150, pady=30, padx=30)
    main_frame.grid(row=2, column=0, columnspan=3)

    file_path = filedialog.askopenfilename()
    lab = main_pro(file_path, main_frame)



top_frame = Frame(root, width=1380, height=150, pady=3, padx=8)
top_frame.grid(row=0, columnspan=3)

header = Label(top_frame, text="prediction system", bg="black", font=20, fg='white', width=13, padx=5, pady=5)
space_header = Label(top_frame, text="", pady=20, padx=20, width=140)
browse_button = Button(top_frame, text="import dataset", command=browse_file, bg="purple", fg="white", border=0,
                       width=13, padx=5, pady=5)

# space = Label(root, text="", pady=30)


header.grid(row=0, column=0)
space_header.grid(row=0, column=1)
browse_button.grid(row=0, column=2)

# space.grid(row=0, column=0, columnspan=3)


root.mainloop()
