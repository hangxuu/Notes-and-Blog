from collections import namedtuple, defaultdict

Grade = namedtuple('Grade', ('score', 'weight'))


class Subject:
    def __init__(self):
        self._grade = []

    def report_grade(self, score, weight):
        self._grade.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grade:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total = 0
        for subject in self._subjects.values():
            total += subject.average_grade()
        return total / len(self._subjects)


class Gradebook:
    def __init__(self):
        self._student = defaultdict(Student)

    def get_student(self, name):
        return self._student[name]


book = Gradebook()
albert = book.get_student('Albert Einstein')
math = albert.get_subject('Math')
math.report_grade(75, 0.05)    # test
math.report_grade(65, 0.15)    # mid term
math.report_grade(70, 0.80)    # final paper
gym = albert.get_subject('Gym')
gym.report_grade(100, 0.40)    # mid term
gym.report_grade(85, 0.60)     # final
print(albert.average_grade())
