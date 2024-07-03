import tkinter as tk
import sqlite3
from tkinter import messagebox

class QuizGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Generator")

        
        self.conn = sqlite3.connect("quiz.db")
        self.c = self.conn.cursor()
        self.create_table()

        
        self.question_label = tk.Label(self.root, text="Question:")
        self.question_label.pack()

        self.question_entry = tk.Entry(self.root, width=50)
        self.question_entry.pack()

        self.answer_label = tk.Label(self.root, text="Answer:")
        self.answer_label.pack()

        self.answer_entry = tk.Entry(self.root, width=50)
        self.answer_entry.pack()

        self.save_button = tk.Button(self.root, text="Save Question", command=self.save_question)
        self.save_button.pack(pady=10)

        self.generate_button = tk.Button(self.root, text="Generate Quiz", command=self.generate_quiz)
        self.generate_button.pack(pady=10)

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS quiz (
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL
                        )""")
        self.conn.commit()

    def save_question(self):
        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()

        if question and answer:
            self.c.execute("INSERT INTO quiz (question, answer) VALUES (?, ?)", (question, answer))
            self.conn.commit()
            self.question_entry.delete(0, tk.END)
            self.answer_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Question saved successfully!")
        else:
            messagebox.showerror("Error", "Please enter both question and answer.")

    def generate_quiz(self):
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Generated Quiz")

        quiz_label = tk.Label(quiz_window, text="Quiz Questions", font=("Helvetica", 16))
        quiz_label.pack()

        self.c.execute("SELECT * FROM quiz")
        questions = self.c.fetchall()

        for idx, (question_id, question, answer) in enumerate(questions, start=1):
            question_label = tk.Label(quiz_window, text=f"{idx}. {question}", wraplength=400, justify="left")
            question_label.pack()

            answer_label = tk.Label(quiz_window, text=f"Answer: {answer}", wraplength=400, justify="left", fg="blue")
            answer_label.pack()

        if not questions:
            no_questions_label = tk.Label(quiz_window, text="No questions available.")
            no_questions_label.pack()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGeneratorApp(root)
    app.run()
