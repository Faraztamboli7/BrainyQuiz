import json
import random

class QuizEngine:
    def __init__(self, question_file):
        with open(question_file, 'r') as f:
            self.questions = json.load(f)
        random.shuffle(self.questions)
        self.index = 0
        self.score = 0

    def has_next(self):
        return self.index < len(self.questions)

    def get_next_question(self):
        if self.has_next():
            return self.questions[self.index]
        return None

    def check_answer(self, selected):
        correct = self.questions[self.index]['answer']
        if selected == correct:
            self.score += 1
            result = True
        else:
            result = False
        self.index += 1
        return result, correct

    def get_score(self):
        return self.score

    def get_total_questions(self):
        return len(self.questions)
