import os
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import functools
import idlelib.tooltip
import file


class GUI:
    def __init__(self):
        self.files = {}
        self.id_list = []
        self.id = 1
        self.temp_id = -1
        self.view_id = 0
        self.root = tkinter.Tk()
        self.root.title("Notepad+")
        self.root.geometry("650x400")
        self.root.minsize(650, 400)
        main_menu = tkinter.Menu(self.root)
        self.f_menu = tkinter.Menu(main_menu, tearoff=0)
        self.f_menu.add_command(label="New", command=self.new_f)
        self.f_menu.add_command(label="Open", command=self.open_f)
        self.f_menu.add_command(label="Save", state="disabled")
        self.f_menu.add_command(label="Save As", state="disabled")
        self.f_menu.add_separator()
        self.f_menu.add_command(label="Exit", command=self.leave_msg)
        self.a_menu = tkinter.Menu(main_menu, tearoff=0)
        self.a_menu.add_command(label="About", command=self.about)
        main_menu.add_cascade(label="File", menu=self.f_menu)
        main_menu.add_cascade(label="Help", menu=self.a_menu)
        self.files_frame = tkinter.Frame(self.root)
        self.placeholder = tkinter.Label(self.root, text="Welcome to Notepad+\nStart editing a file by clicking 'File "
                                                         "-> New' or 'File -> Open'")
        self.placeholder.pack()
        self.left = tkinter.Button(self.files_frame, text="<", command=self.shift_left)
        self.right = tkinter.Button(self.files_frame, text=">", command=self.shift_right)
        self.scroll_bar = None
        self.field = None
        self.root.config(menu=main_menu)
        self.root.protocol("WM_DELETE_WINDOW", self.leave_msg)
        self.root.mainloop()

    def about(self):
        self.a_menu.entryconfigure(0, state="disabled")
        window = tkinter.Toplevel()
        window.title("About")
        window.geometry("250x350")
        window.minsize(250, 350)
        scroll = tkinter.Scrollbar(window)
        scroll.pack(side="right", fill="y")
        text = tkinter.Text(window, yscrollcommand=scroll.set)
        text.pack(expand=True, fill="both")
        scroll.config(command=text.yview)
        text.insert("end", "Made using the Python\nprogramming language, GUI made\nusing the tkinter library.")
        text.config(state="disabled")
        window.protocol("WM_DELETE_WINDOW", lambda: (window.destroy(), self.a_menu.entryconfigure(0, state="normal")))

    def leave_msg(self):
        if tkinter.messagebox.askyesno("Leave Notepad+?", "Unsaved changes will be lost!"):
            self.root.destroy()

    def create_field(self):
        self.placeholder.pack_forget()
        self.files_frame.pack()
        self.scroll_bar = tkinter.Scrollbar(self.root)
        self.scroll_bar.pack(side="right", fill="y")
        self.field = tkinter.Text(self.root, yscrollcommand=self.scroll_bar.set)
        self.field.pack(expand=True, fill="both")
        self.scroll_bar.config(command=self.field.yview)

    def star(self, this_id, event=None):
        if not self.files[this_id][4]:
            self.files[this_id][4] = True
            self.files[this_id][1]["text"] = "*" + self.files[this_id][1]["text"]

    def save_text(self):
        self.files[self.temp_id][0].data = self.field.get("1.0", "end")
        self.field.delete("1.0", "end")
        self.files[self.temp_id][1].config(background="grey")
        self.files[self.temp_id][2].config(background="grey", state="disabled")
        self.files[self.temp_id][3] = self.scroll_bar.get()

    def new_f(self):
        if self.files == {}:
            self.create_field()
        if self.temp_id > -1:
            self.save_text()
        self.field.unbind("<Key>")
        self.files[self.id] = [file.File("new" + str(self.id)),
                               tkinter.Button(self.files_frame,
                                              text="new" + str(self.id),
                                              background="white",
                                              command=functools.partial(self.change_f, self.id)),
                               tkinter.Button(self.files_frame,
                                              text="x",
                                              background="red",
                                              command=functools.partial(self.close_f, self.id)),
                               None,
                               False]
        if len(self.files[self.id][1]["text"]) > 10:
            self.files[self.id][1]["text"] = "new"
        self.f_menu.entryconfigure(2, command=functools.partial(self.save_f, self.id), state="normal")
        self.f_menu.entryconfigure(3, command=functools.partial(self.save_f_as, self.id), state="normal")
        self.field.bind("<Key>", functools.partial(self.star, self.id))
        self.id_list.append(self.id)
        self.pack_buttons(self.id)
        self.temp_id = self.id
        self.id += 1

    def change_f(self, this_id):
        if self.temp_id > -1:
            self.save_text()
        self.temp_id = this_id
        self.field.unbind("<Key>")
        self.field.bind("<Key>", functools.partial(self.star, this_id))
        self.field.insert("end", self.files[this_id][0].data[0:-1])
        self.files[this_id][1].config(background="white")
        self.files[this_id][2].config(background="red", state="normal")
        self.field.yview_moveto(str(self.files[this_id][3][0]))
        self.f_menu.entryconfigure(2, command=functools.partial(self.save_f, this_id), state="normal")
        self.f_menu.entryconfigure(3, command=functools.partial(self.save_f_as, this_id), state="normal")

    def open_f(self):
        try:
            path = tkinter.filedialog.askopenfilename(title="Open", filetypes=[("Text Files", ".txt")])
            path = os.path.normpath(path)
            if path != "." and path.endswith(".txt"):
                if self.files == {}:
                    self.create_field()
                if self.temp_id > -1:
                    self.save_text()
                name = path.split("\\")[-1]
                self.files[self.id] = [file.File(name),
                                       tkinter.Button(self.files_frame,
                                                      text=name,
                                                      background="white",
                                                      command=functools.partial(self.change_f, self.id)),
                                       tkinter.Button(self.files_frame,
                                                      text="x",
                                                      background="red",
                                                      command=functools.partial(self.close_f, self.id)),
                                       None,
                                       False]
                self.files[self.id][0].set_path(name, path)
                self.f_menu.entryconfigure(2, command=functools.partial(self.save_f, self.id), state="normal")
                self.f_menu.entryconfigure(3, command=functools.partial(self.save_f_as, self.id), state="normal")
                self.id_list.append(self.id)
                input_f = open(path, "r", encoding="utf8")
                self.field.insert("end", input_f.read())
                input_f.close()
                idlelib.tooltip.Hovertip(self.files[self.id][1], path)
                self.pack_buttons(self.id)
                self.field.unbind("<Key>")
                self.field.bind("<Key>", functools.partial(self.star, self.id))
                self.temp_id = self.id
                self.id += 1
        except:
            tkinter.messagebox.showerror("Error", "Something went wrong when opening the file.")

    def close_f(self, this_id):
        if self.files[this_id][4]:
            if tkinter.messagebox.askyesno("Save Changes?", "Changes made to this file will be lost! Save changes?"):
                self.save_f(this_id)
        self.temp_id = -1
        self.files[this_id][1].destroy()
        self.files[this_id][2].destroy()
        self.files.pop(this_id, None)
        if len(self.id_list) == 1:
            self.files.pop(this_id, None)
            self.id_list.pop()
            self.scroll_bar.pack_forget()
            self.field.pack_forget()
            self.left.pack_forget()
            self.right.pack_forget()
            self.files_frame.pack_forget()
            self.placeholder.pack()
            self.f_menu.entryconfigure(2, state="disabled")
            self.f_menu.entryconfigure(3, state="disabled")
        else:
            if self.id_list.index(this_id) == 0:
                next_id = self.id_list[self.id_list.index(this_id) + 1]
            else:
                next_id = self.id_list[self.id_list.index(this_id) - 1]
            self.field.delete("1.0", "end")
            self.change_f(next_id)
            self.id_list.pop(self.id_list.index(this_id))
            self.pack_buttons(next_id)
        self.field.unbind("<Key>")

    def save_f(self, this_id):
        try:
            if not self.files[this_id][0].saved:
                path = tkinter.filedialog.asksaveasfilename(title="Save", filetypes=[("Text Files", ".txt")])
                if path != "":
                    path = os.path.normpath(path)
                    path += ".txt"
                    out_file = open(path, "w", encoding="utf8")
                    out_file.write(self.field.get("1.0", "end")[0:-1])
                    out_file.close()
                    name = path.split("\\")[-1]
                    self.files[this_id][0].set_path(name, path)
                    self.files[this_id][1].config(text=name[0:10])
                    idlelib.tooltip.Hovertip(self.files[this_id][1], path)
                    self.files[this_id][4] = False
            else:
                out_file = open(self.files[this_id][0].get_path(), "w", encoding="utf8")
                out_file.write(self.field.get("1.0", "end")[0:-1])
                out_file.close()
                if self.files[this_id][4]:
                    self.files[this_id][4] = False
                    self.files[this_id][1]["text"] = (self.files[this_id][1]["text"])[1:]
        except:
            tkinter.messagebox.showerror("Error", "Something went wrong when saving the file.")

    def save_f_as(self, this_id):
        try:
            path = tkinter.filedialog.asksaveasfilename(title="Save As", filetypes=[("Text Files", ".txt")])
            if path != "":
                path = os.path.normpath(path)
                path += ".txt"
                out_file = open(path, "w", encoding="utf8")
                out_file.write(self.field.get("1.0", "end")[0:-1])
                out_file.close()
                name = path.split("\\")[-1]
                self.files[this_id][0].set_path(name, path)
                self.files[this_id][1].config(text=name[0:10])
                idlelib.tooltip.Hovertip(self.files[this_id][1], path)
                self.files[this_id][4] = False
        except:
            tkinter.messagebox.showerror("Error", "Something went wrong when saving the file.")

    def pack_buttons(self, this_id=None):
        if this_id is not None:
            self.view_id = self.id_list.index(this_id) // 5 * 5
        for w in self.files_frame.winfo_children():
            w.pack_forget()
        self.left.pack(side="left")
        for i in range(self.view_id, self.view_id + 5):
            try:
                self.files[self.id_list[i]][1].pack(side="left")
                self.files[self.id_list[i]][2].pack(side="left")
            except IndexError:
                break
        self.right.pack(side="left")

    def shift_left(self):
        if self.view_id > 4:
            self.view_id -= 5
        self.pack_buttons()

    def shift_right(self):
        if self.view_id < len(self.id_list) - 5:
            self.view_id += 5
        self.pack_buttons()


if __name__ == "__main__":
    GUI()
