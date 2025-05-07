import tkinter as tk
from tkinter import messagebox
from quiz_engine import QuizEngine

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BrainyQuiz")
        self.window.geometry("500x400")
        self.quiz = QuizEngine("questions.json")
        self.timer_id = None
        self.time_left = 30

        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.window, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):
            btn = tk.Button(self.window, text="", width=40, command=lambda i=i: self.select_option(i))
            btn.pack(pady=5)
            self.options.append(btn)

        self.timer_label = tk.Label(self.window, text="Time left: 30", font=("Arial", 12))
        self.timer_label.pack(pady=10)

    def load_question(self):
        if self.quiz.has_next():
            self.time_left = 30
            self.update_timer()
            q = self.quiz.get_next_question()
            self.current_answer = q['answer']
            self.question_label.config(text=q['question'])
            for i, opt in enumerate(q['options']):
                self.options[i].config(text=opt, state=tk.NORMAL)
        else:
            self.end_quiz()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.quiz.index += 1
            self.load_question()

    def select_option(self, index):
        selected = self.options[index].cget("text")
        result, correct = self.quiz.check_answer(selected)
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        if result:
            messagebox.showinfo("Correct!", "Good job!")
        else:
            messagebox.showerror("Wrong!", f"Correct answer: {correct}")
        self.load_question()

    def end_quiz(self):
        score = self.quiz.get_score()
        total = self.quiz.get_total_questions()
        messagebox.showinfo("Quiz Over", f"Your Score: {score}/{total}")
        self.window.destroy()

    def run(self):
        self.window.mainloop()
