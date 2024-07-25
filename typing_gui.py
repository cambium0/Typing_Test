from tkinter import *
from tkinter.ttk import Frame, Combobox
from tkinter import messagebox
import time
import threading
import prepare_test_file as ptf


class Timer:
    def __init__(self, duration, test_obj):
        self.duration = duration
        self.test_obj = test_obj

    def countdown(self):
        while self.duration > 0:
            time.sleep(1)
            self.duration -= 1
            self.test_obj.field2.delete('0', END)
            self.test_obj.field2.insert('0', str(self.duration))
        cpm, wpm = self.test_obj.score_test()
        self.test_obj.text_window.delete('1.0', END)
        self.test_obj.text_window.pack_forget()
        self.test_obj.field0.delete(0, 'end')
        self.test_obj.field0.insert(0, cpm)
        self.test_obj.field1.delete(0, 'end')
        self.test_obj.field1.insert(0, wpm)
        self.test_obj.label4.pack()
        self.test_obj.label5.pack(side='left', padx=16, pady=20)
        self.test_obj.label6.pack(side='left')
        self.test_obj.label6.configure(text=cpm)
        self.test_obj.label7.pack(side='left', padx=16, pady=20)
        self.test_obj.label8.pack(side='left')
        self.test_obj.label8.configure(text=wpm)

        return

    def start_timer(self):
        my_thread = threading.Thread(target=self.countdown)
        my_thread.start()


class TypingTester:

    words = ""
    text = ""
    text_pos = 1.0
    first_stroke = True
    test_end = False
    overflow = 0  # counts the number of index tics user types beyond a word but before pressing spacebar; must be
                  # nullified by on_back before on_back begins to decrement self.text_pos
    line_starts = [0]
    start_index = 0
    correct_chars = 0
    correct_words = 0

    def set_input_text(self):
        # center the text, center the cursor
        self.input.icursor(9)

    def restart_test(self):
        difficulty = self.combo0.get()
        self.text = ptf.make_test_text(self.words, difficulty)
        self.field0.delete(0, 'end')
        self.field0.insert(0, '0')
        self.field1.delete(0, 'end')
        self.field1.insert(0, '0')
        self.field2.delete(0, 'end')
        self.field2.insert(0, '60')
        self.input.delete(0, 'end')
        self.input.insert(0, 'type the words here')
        self.input.icursor(9)
        self.label4.pack_forget()
        self.label5.pack_forget()
        self.label5.pack_forget()
        self.label6.pack_forget()
        self.label7.pack_forget()
        self.label8.pack_forget()
        self.text_window.pack()
        self.text_window.delete('1.0', END)
        self.text_window.insert('1.0', self.text)
        self.input.bind('<Key>', self.keystroke)
        self.input.bind('<Return>', self.on_enter)
        self.input.bind('<BackSpace>', self.on_back)
        self.text_window.tag_add('word_highlite', '1.0 wordstart', '1.0 wordend')
        self.text_window.tag_configure('word_highlite', background='#229922', foreground='#000000', font="TkFixedFont")
        self.text_window.tag_add('red_char', END)
        self.text_window.tag_configure('red_char', foreground="#aa2222", font="TkFixedFont")
        self.text_window.tag_add('white_char', END)
        self.text_window.tag_configure('white_char', foreground="#efefef", font="TkFixedFont")
        self.text_window.tag_add('red_word', END)
        self.text_window.tag_configure('red_word', foreground="#aa2222", font="TkFixedFont")
        self.text_window.tag_add('blue_word', END)
        self.text_window.tag_configure('blue_word', foreground="#2222bb", font="TkFixedFont")
        self.text_pos = 1.0
        self.first_stroke = True
        self.test_end = False
        self.overflow = 0  # counts the number of index tics user types beyond a word but before pressing spacebar; must be
                      # nullified by on_back before on_back begins to decrement self.text_pos
        self.line_starts = [0]
        self.start_index = 0
        self.correct_chars = 0
        self.correct_words = 0

    def on_enter(self, event):
        messagebox.showinfo("Attention!",
                            "User the space bar rather than enter. It's faster. Use the 'restart' button to start over.")

    def contains(self, atup, phrase): # passed a tuple containing tag names for a given index, try to match the 'phrase' (a tag name)
        for item in atup:
            if item == phrase:
                return True
        return False

    def get_line_and_char_num_from_range(self, a_range):
        line_num_start, word_char_start = str(a_range[0]).split('.')
        reducer = len(str(a_range[1])) - 2
        num_cees = str(a_range[1])[-reducer:]
        int_num_cees = int(num_cees)
        int_word_start = int(word_char_start)
        return line_num_start, word_char_start, num_cees, int_num_cees, int_word_start

    def is_char(self, an_index):
        if self.text_window.get(an_index) != ' ':
            return True
        else:
            return False

    def score_test(self):
        last = '1.0'
        addend = 0
        ranges = self.text_window.tag_ranges('blue_word')
        self.correct_words = len(ranges)
        for val in ranges:
            val_string = str(val)
            last_string = str(last)
            addend = int(val_string[2:]) - int(last_string[2:])
            self.correct_chars += addend
            last = val
        return self.correct_chars, self.correct_words

    def char_at(self, an_index):
        a_char = self.text_window.get(an_index)
        return a_char

    def set_line_start(self):
        text_pos = int(self.text_window.index(f"{self.text_pos} + 1c").split('.')[1])
        self.start_index += 1
        if text_pos not in self.line_starts:
            self.line_starts.append(text_pos)

    def check_newline(self, a_word):
        int_num_cees = int(a_word[1].split('.')[1])
        next_word_start = self.text_window.index(f"{self.text_pos} + 2c")
        next_word = self.get_word_range_from_index(next_word_start)
        next_word_end_index = int(next_word[1].split('.')[1])
        try:
            start_index = self.line_starts[self.start_index]
        except IndexError:
            print(f"IndexError: index was {self.start_index}")
            exit(1)
        my_line_start = self.line_starts[self.start_index]
        if next_word_end_index > self.line_starts[self.start_index] + 40 and int(self.text_pos.split('.')[1]) > 40:
            return True
        elif next_word_end_index > self.line_starts[self.start_index] + 40 and int(self.text_pos.split('.')[1]) <= 40:
            self.set_line_start()
            return False
        else:
            return False

    def get_word_range_from_index(self, an_index):
        word_range = self.text_window.index(f"{an_index} wordstart"), self.text_window.index(f"{an_index} wordend")
        return word_range

    def on_back(self, event):
        prev_index = self.text_pos
        if self.line_starts[self.start_index] == int(self.text_pos.split('.')[1]):
            line_start = self.line_starts[self.start_index]
            text_pos = int(self.text_pos.split('.')[1])
            self.text_window.yview("scroll", -1, 'units')
            self.start_index -= 1
        if self.overflow > 0:
            self.overflow -= 1
            return
        self.text_pos = self.text_window.index(f"{self.text_pos} - 1c")
        if not self.is_char(self.text_pos):
            next_index = self.text_window.index(f"{self.text_pos} - 1c")
            prev_word = self.get_word_range_from_index(prev_index)
            self.text_window.tag_remove('word_highlite', prev_word[0], prev_word[1])
            next_word = self.get_word_range_from_index(next_index)
            self.text_window.tag_add('word_highlite', next_word[0], next_word[1])
            self.text_window.tag_remove('blue_word', next_word[0], next_word[1])
            self.text_window.tag_remove('red_char', f"{self.text_pos}")
            self.text_window.tag_remove('white_char', f"{self.text_pos}")
        else:
            self.text_window.tag_remove('red_char', f"{self.text_pos}")
            self.text_window.tag_remove('white_char', f"{self.text_pos}")
            this_word = self.get_word_range_from_index(self.text_pos)
            self.text_window.tag_remove('red_word', this_word[0], this_word[1])

    def keystroke(self, event):
        word = ""
        if self.char_at(self.text_pos) != ' ':
            word = self.get_word_range_from_index(self.text_pos)
        else:
            prev_index = self.text_window.index(f"{self.text_pos} - 1c")
            word = self.get_word_range_from_index(prev_index)
        if self.first_stroke:
            self.input.delete('0', END)
            self.first_stroke = False
            typing_timer = Timer(60, self)
            typing_timer.start_timer()
        if event.char == ' ':
            if self.check_newline(word):
                self.text_window.yview("scroll", 1, 'units')
                self.set_line_start()
            self.text_pos = self.text_window.index(f"{self.text_pos} + 1c")
            next_index = self.text_window.index(f"{self.text_pos} + 1c")
            prev_index = self.text_window.index(f"{self.text_pos} - 2c")
            if f"{self.text_window.index}" == f"{self.text_window.index('end')}":
                self.test_end = True
            else:
                word = self.get_word_range_from_index(prev_index)
                self.text_window.tag_remove('word_highlite', word[0], word[1])
                line_num_start, word_char_start, num_cees, int_num_cees, int_word_start = self.get_line_and_char_num_from_range(word)
                red_word_tag = False
                for i in range(int_word_start, int_num_cees):
                    i_dec = line_num_start + '.' + str(i)
                    tag_names = self.text_window.tag_names(i_dec)
                    if len(tag_names) == 0 or self.text_window.tag_names(i_dec)[0] == 'red_char':
                        self.text_window.tag_add('red_word', word[0], word[1])
                        red_word_tag = True
                        break
                    if self.text_window.tag_names(i_dec)[0] == 'red_char':
                        self.text_window.tag_add('red_word', word[0], word[1])
                        red_word_tag = True
                        break
                if not red_word_tag:
                    self.text_window.tag_add('blue_word', word[0], word[1])
            self.input.delete('0', END)
            self.input.focus()
            self.input.icursor(-1)
            self.text_pos = self.text_window.index(f"{word[1]} + 1c")
            self.text_window.tag_add('word_highlite', f"{self.text_pos} wordstart", f"{self.text_pos} wordend")
        elif event.char in list(map(chr, range(65, 90))) or list(map(chr, range(97, 123))):
            line_num_start, word_char_start, num_cees, int_num_cees, int_word_start = self.get_line_and_char_num_from_range(word)
            if int(str(self.text_pos).split('.')[1]) == int_num_cees:
                self.overflow += 1
                return
            self.text_pos = self.text_window.index(f"{self.text_pos} + 1c")
            text_char = self.text_window.get(f"{self.text_pos} - 1c")
            if text_char == event.char:
                self.text_window.tag_add('white_char', f"{self.text_pos}-1c")
                try:
                    self.text_window.tag_remove('red_char', f"{self.text_pos}-1c")
                except:
                    print("tried to remove a red tag when there was none")
            else:
                self.text_window.tag_add('red_char', f"{self.text_pos}-1c")
                try:
                    self.text_window.tag_remove('white_char', f"{self.text_pos}-1c")
                except:
                    print("tried to remove a white tag when there was none")

    window = Tk()
    window.geometry("580x590")
    label0 = Label(window, text="Typing Test", fg="blue", font=("Arial", 32, "normal"))
    frame0 = Frame(window)
    label1 = Label(frame0, text="Corrected CPM: ", font=("sans-serif", 12, "normal"))
    field0 = Entry(frame0, width=3)
    label2 = Label(frame0, text="WPM: ", font=("sans-serif", 12, "normal"))
    field1 = Entry(frame0, width=3)
    label3 = Label(frame0, text="Time left: ", font=("sans-serif", 12, "normal"))
    field2 = Entry(frame0, width=3)
    button0 = Button(window, text="restart", font=("sans-serif", 12, "normal"), fg="red")
    combo0 = Combobox(window, state="readonly", values=["easy", "moderate", "hard"])
    frame1 = Frame(window)
    text_window = Text(frame1, fg="#223322", height=3, width=40, font="TkFixedFont", padx=12,
                       pady=12, wrap=WORD)
    label4 = Label(frame1, text="Your Score:", font=("san-serif", 24, "normal"))
    label5 = Label(frame1, text="CPM: ", font=("sans-serif", 14, "normal"))
    label6 = Label(frame1, text="", font=("sans-serif", 14, "italic"))
    label7 = Label(frame1, text="WPM: ", font=("sans-serif", 14, "normal"))
    label8 = Label(frame1, text="", font=("sans-serif", 14, "italic"))
    input = Entry(window, width=40, justify=CENTER, font=('serif', 18, 'normal'))

    def pack_widgets(self):
        print(self.text)
        self.label0.pack(pady=24)
        self.frame0.pack(pady=24)
        self.label1.pack(side='left', padx=6)
        self.field0.pack(side='left', padx=6)
        self.field0.insert(END, '0')
        self.label2.pack(side='left', padx=6)
        self.field1.pack(side='left', padx=6)
        self.field1.insert(END, '0')
        self.label3.pack(side='left', padx=6)
        self.field2.pack(side='left', padx=6)
        self.field2.insert(END, '60')
        self.combo0.pack(pady=12)
        self.combo0.set('moderate')
        self.frame1.pack()
        self.text_window.pack(pady=24)
        self.text_window.insert(END, self.text)
        self.input.pack(padx=12, pady=24)
        self.input.insert(15, "type the words here")
        self.input.icursor(9)
        self.input.bind('<Key>', self.keystroke)
        self.input.bind('<Return>', self.on_enter)
        self.input.bind('<BackSpace>', self.on_back)
        self.button0.pack(pady=24)
        self.button0.configure(command=self.restart_test)
        self.text_window.tag_add('word_highlite', '1.0 wordstart', '1.0 wordend')
        self.text_window.tag_configure('word_highlite', background='#229922', foreground='#000000', font="TkFixedFont")
        self.text_window.tag_add('red_char', END)
        self.text_window.tag_configure('red_char', foreground="#aa2222", font="TkFixedFont")
        self.text_window.tag_add('white_char', END)
        self.text_window.tag_configure('white_char', foreground="#efefef", font="TkFixedFont")
        self.text_window.tag_add('red_word', END)
        self.text_window.tag_configure('red_word', foreground="#aa2222", font="TkFixedFont")
        self.text_window.tag_add('blue_word', END)
        self.text_window.tag_configure('blue_word', foreground="#2222bb", font="TkFixedFont")

    def __init__(self, text, test_dict):
        self.text = text
        self.words = test_dict
        self.pack_widgets()

