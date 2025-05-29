import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# Database setup
DB_FILE = 'quiz_game.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Ensure questions table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer INTEGER NOT NULL,
    hint TEXT
)
''')
conn.commit()

def insert_questions(questions):
    for q in questions:
        cursor.execute('''SELECT COUNT(*) FROM questions WHERE category=? AND question=?''', (q[0], q[1]))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''INSERT INTO questions (category, question, option1, option2, option3, option4, answer, hint) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', q)
    conn.commit()

algorithms_questions = [
    ('Algorithms', 'What is the time complexity of binary search?', 'O(n)', 'O(log n)', 'O(n^2)', 'O(1)', 2, 'Divides the list in half each step.'),
    ('Algorithms', 'Which sorting algorithm is fastest on average?', 'Bubble Sort', 'Quick Sort', 'Merge Sort', 'Insertion Sort', 2, 'Divide and conquer strategy.'),
    ('Algorithms', 'Which algorithm uses backtracking?', 'Dijkstra', 'BFS', 'DFS', 'N-Queens', 4, 'It recursively tries and rolls back.'),
    ('Algorithms', 'Which algorithm finds the shortest path?', 'Bellman-Ford', 'Dijkstra', 'Floyd-Warshall', 'All of these', 4, 'All are used in shortest path problems.'),
    ('Algorithms', 'Which algorithm is used for minimum spanning tree?', "Prim's", "Kruskal's", "Boruvka's", 'All of these', 4, 'All are MST algorithms.'),
    ('Algorithms', 'Which is a divide and conquer algorithm?', 'Bubble Sort', 'Quick Sort', 'Selection Sort', 'Insertion Sort', 2, 'It divides and sorts subarrays.'),
    ('Algorithms', 'Which algorithm is used for topological sorting?', 'DFS', 'BFS', 'Dijkstra', 'Bellman-Ford', 1, 'DFS is used for topological order.'),
    ('Algorithms', 'Which algorithm is NOT greedy?', "Prim's", "Kruskal's", "Dijkstra", 'Floyd-Warshall', 4, 'Floyd-Warshall is dynamic programming.'),
    ('Algorithms', 'Which algorithm solves the knapsack problem optimally?', 'Greedy', 'Dynamic Programming', 'DFS', 'BFS', 2, 'DP gives optimal solution.'),
    ('Algorithms', 'Which is used for cycle detection in graphs?', 'DFS', 'BFS', 'Dijkstra', 'Bellman-Ford', 1, 'DFS can detect cycles.')
]

databases_questions = [
    ('Databases', 'Which SQL statement is used to extract data from a database?', 'GET', 'OPEN', 'SELECT', 'EXTRACT', 3, 'SELECT is used to retrieve data.'),
    ('Databases', 'Which command is used to remove all records from a table?', 'DELETE', 'REMOVE', 'DROP', 'TRUNCATE', 4, 'TRUNCATE removes all rows, keeping the table.'),
    ('Databases', 'Which is a NoSQL database?', 'MySQL', 'MongoDB', 'PostgreSQL', 'Oracle', 2, 'MongoDB is document-based.'),
    ('Databases', 'What does ACID stand for?', 'Atomicity, Consistency, Isolation, Durability', 'Accuracy, Consistency, Isolation, Durability', 'Atomicity, Concurrency, Isolation, Durability', 'Atomicity, Consistency, Integration, Durability', 1, 'ACID is a set of properties for transactions.'),
    ('Databases', 'Which SQL clause is used to filter results?', 'ORDER BY', 'WHERE', 'GROUP BY', 'HAVING', 2, 'WHERE filters rows.'),
    ('Databases', 'Which key uniquely identifies a record?', 'Foreign Key', 'Primary Key', 'Unique Key', 'Super Key', 2, 'Primary Key is unique.'),
    ('Databases', 'Which normal form removes partial dependency?', '1NF', '2NF', '3NF', 'BCNF', 2, '2NF removes partial dependency.'),
    ('Databases', 'Which command is used to add a new row?', 'INSERT', 'ADD', 'APPEND', 'UPDATE', 1, 'INSERT adds new rows.'),
    ('Databases', 'Which SQL function returns the number of rows?', 'COUNT()', 'SUM()', 'TOTAL()', 'NUMBER()', 1, 'COUNT() returns row count.'),
    ('Databases', 'Which JOIN returns all records from both tables?', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN', 4, 'FULL OUTER JOIN returns all records.')
]

general_questions = [
    ('General', 'What does CPU stand for?', 'Central Processing Unit', 'Central Programming Unit', 'Computer Processing Unit', 'Central Performance Unit', 1, 'CPU is the brain of the computer.'),
    ('General', 'Which language is used for web apps?', 'Python', 'JavaScript', 'C++', 'All of these', 4, 'All can be used for web apps.'),
    ('General', 'What is the extension for Python files?', '.py', '.java', '.cpp', '.txt', 1, 'Python files end with .py'),
    ('General', 'Which device is used to input data?', 'Monitor', 'Printer', 'Keyboard', 'Speaker', 3, 'Keyboard is an input device.'),
    ('General', 'What is RAM?', 'Read Access Memory', 'Random Access Memory', 'Run Access Memory', 'Random Actual Memory', 2, 'RAM is volatile memory.'),
    ('General', 'Which protocol is used for web?', 'HTTP', 'FTP', 'SMTP', 'SSH', 1, 'HTTP is for web.'),
    ('General', 'Which is not an OS?', 'Windows', 'Linux', 'Oracle', 'MacOS', 3, 'Oracle is a database.'),
    ('General', 'What is the binary of 2?', '10', '11', '01', '00', 1, '2 in binary is 10.'),
    ('General', 'Which is a search engine?', 'Google', 'Facebook', 'Twitter', 'Instagram', 1, 'Google is a search engine.'),
    ('General', 'Which is a programming paradigm?', 'OOP', 'POP', 'Functional', 'All of these', 4, 'All are paradigms.')
]

compilers_questions = [
    ('Compilers', 'What is the first phase of a compiler?', 'Lexical Analysis', 'Syntax Analysis', 'Semantic Analysis', 'Code Generation', 1, 'It breaks input into tokens.'),
    ('Compilers', 'Which data structure is used for syntax analysis?', 'Stack', 'Queue', 'Tree', 'Graph', 3, 'Parse trees are used.'),
    ('Compilers', 'Which phase checks for grammar errors?', 'Lexical', 'Syntax', 'Semantic', 'Optimization', 2, 'Syntax analysis checks grammar.'),
    ('Compilers', 'Which phase checks for meaning?', 'Lexical', 'Syntax', 'Semantic', 'Code Generation', 3, 'Semantic analysis checks meaning.'),
    ('Compilers', 'Which is not a compiler phase?', 'Lexical', 'Linking', 'Syntax', 'Semantic', 2, 'Linking is after compilation.'),
    ('Compilers', 'Which tool generates lexical analyzers?', 'YACC', 'LEX', 'Bison', 'Flex', 2, 'LEX is for lexical analysis.'),
    ('Compilers', 'Which is a bottom-up parser?', 'LL', 'LR', 'Recursive Descent', 'Predictive', 2, 'LR is bottom-up.'),
    ('Compilers', 'Which phase generates intermediate code?', 'Lexical', 'Syntax', 'Intermediate Code Generation', 'Optimization', 3, 'It comes after semantic analysis.'),
    ('Compilers', 'Which is used for code optimization?', 'Peephole', 'Syntax', 'Lexical', 'Semantic', 1, 'Peephole optimization is common.'),
    ('Compilers', 'Which phase produces target code?', 'Code Generation', 'Lexical', 'Syntax', 'Semantic', 1, 'Final phase is code generation.')
]

os_questions = [
    ('Operating Systems', 'Which is not an OS?', 'Windows', 'Linux', 'Oracle', 'MacOS', 3, 'Oracle is a database.'),
    ('Operating Systems', 'Which is a real-time OS?', 'Windows', 'Linux', 'RTOS', 'DOS', 3, 'RTOS is real-time.'),
    ('Operating Systems', 'Which manages memory?', 'Compiler', 'OS', 'Assembler', 'Linker', 2, 'OS manages memory.'),
    ('Operating Systems', 'Which is not a scheduling algorithm?', 'FCFS', 'SJF', 'LRU', 'Round Robin', 3, 'LRU is for paging.'),
    ('Operating Systems', 'Which is not a file system?', 'NTFS', 'FAT', 'EXT', 'FTP', 4, 'FTP is a protocol.'),
    ('Operating Systems', 'Which is not a process state?', 'Ready', 'Running', 'Waiting', 'Executing', 4, 'Executing is not a state.'),
    ('Operating Systems', 'Which is not a deadlock condition?', 'Mutual Exclusion', 'Hold and Wait', 'Preemption', 'Circular Wait', 3, 'Preemption prevents deadlock.'),
    ('Operating Systems', 'Which is not a type of OS?', 'Batch', 'Time Sharing', 'Distributed', 'Compiler', 4, 'Compiler is not an OS.'),
    ('Operating Systems', 'Which is not a memory management technique?', 'Paging', 'Segmentation', 'Swapping', 'Compiling', 4, 'Compiling is not memory management.'),
    ('Operating Systems', 'Which is not an interrupt?', 'Hardware', 'Software', 'Spurious', 'Compiler', 4, 'Compiler is not an interrupt.')
]

data_structures_questions = [
    ('Data Structures', 'Which is a linear data structure?', 'Tree', 'Graph', 'Stack', 'Heap', 3, 'Stack is linear.'),
    ('Data Structures', 'Which is not a dynamic data structure?', 'Array', 'Linked List', 'Stack', 'Queue', 1, 'Array is static.'),
    ('Data Structures', 'Which is used for BFS?', 'Stack', 'Queue', 'Tree', 'Graph', 2, 'Queue is used for BFS.'),
    ('Data Structures', 'Which is not a tree traversal?', 'Inorder', 'Preorder', 'Postorder', 'Middleorder', 4, 'Middleorder does not exist.'),
    ('Data Structures', 'Which is not a sorting algorithm?', 'Bubble', 'Quick', 'Binary', 'Merge', 3, 'Binary is not sorting.'),
    ('Data Structures', 'Which is not a graph?', 'Directed', 'Undirected', 'Weighted', 'Circular', 4, 'Circular is not a graph type.'),
    ('Data Structures', 'Which is not a stack operation?', 'Push', 'Pop', 'Peek', 'Insert', 4, 'Insert is not stack operation.'),
    ('Data Structures', 'Which is not a queue type?', 'Simple', 'Circular', 'Priority', 'Binary', 4, 'Binary is not a queue.'),
    ('Data Structures', 'Which is not a heap?', 'Min', 'Max', 'Binary', 'Linear', 4, 'Linear is not a heap.'),
    ('Data Structures', 'Which is not a linked list?', 'Singly', 'Doubly', 'Circular', 'Binary', 4, 'Binary is not a linked list.')
]

networking_questions = [
    ('Networking', 'Which is not a network topology?', 'Star', 'Bus', 'Ring', 'Circle', 4, 'Circle is not a topology.'),
    ('Networking', 'Which protocol is used for web?', 'HTTP', 'FTP', 'SMTP', 'SSH', 1, 'HTTP is for web.'),
    ('Networking', 'Which is not a layer in OSI?', 'Physical', 'Data Link', 'Internet', 'Transport', 3, 'Internet is not in OSI.'),
    ('Networking', 'Which device connects networks?', 'Switch', 'Router', 'Hub', 'Repeater', 2, 'Router connects networks.'),
    ('Networking', 'Which is not a protocol?', 'TCP', 'UDP', 'IP', 'HTML', 4, 'HTML is not a protocol.'),
    ('Networking', 'Which is not a transmission medium?', 'Twisted Pair', 'Coaxial', 'Fiber', 'Router', 4, 'Router is a device.'),
    ('Networking', 'Which is not a wireless technology?', 'WiFi', 'Bluetooth', 'Ethernet', 'Infrared', 3, 'Ethernet is wired.'),
    ('Networking', 'Which is not an IP address class?', 'A', 'B', 'C', 'F', 4, 'F is not a class.'),
    ('Networking', 'Which is not a valid IP?', '192.168.1.1', '256.1.1.1', '10.0.0.1', '172.16.0.1', 2, '256 is invalid.'),
    ('Networking', 'Which is not a DNS record?', 'A', 'MX', 'CNAME', 'FTP', 4, 'FTP is not a DNS record.')
]

software_eng_questions = [
    ('Software Engineering', 'Which is not a SDLC model?', 'Waterfall', 'Agile', 'Spiral', 'Binary', 4, 'Binary is not a model.'),
    ('Software Engineering', 'Which is not a requirement type?', 'Functional', 'Non-Functional', 'Technical', 'Physical', 4, 'Physical is not a requirement.'),
    ('Software Engineering', 'Which is not a UML diagram?', 'Class', 'Sequence', 'Flowchart', 'Activity', 3, 'Flowchart is not UML.'),
    ('Software Engineering', 'Which is not a testing type?', 'Unit', 'Integration', 'System', 'Binary', 4, 'Binary is not a testing type.'),
    ('Software Engineering', 'Which is not a design principle?', 'SOLID', 'DRY', 'KISS', 'BINARY', 4, 'BINARY is not a principle.'),
    ('Software Engineering', 'Which is not a process model?', 'Waterfall', 'Agile', 'RAD', 'Binary', 4, 'Binary is not a model.'),
    ('Software Engineering', 'Which is not a maintenance type?', 'Corrective', 'Adaptive', 'Perfective', 'Binary', 4, 'Binary is not a maintenance type.'),
    ('Software Engineering', 'Which is not a project management tool?', 'Gantt', 'PERT', 'Binary', 'CPM', 3, 'Binary is not a tool.'),
    ('Software Engineering', 'Which is not a risk?', 'Technical', 'Schedule', 'Binary', 'Cost', 3, 'Binary is not a risk.'),
    ('Software Engineering', 'Which is not a documentation type?', 'User', 'System', 'Binary', 'Technical', 3, 'Binary is not a documentation type.')
]

# Insert questions if not already present
insert_questions(algorithms_questions)
insert_questions(databases_questions)
insert_questions(general_questions)
insert_questions(compilers_questions)
insert_questions(os_questions)
insert_questions(data_structures_questions)
insert_questions(networking_questions)
insert_questions(software_eng_questions)

def get_categories():
    cursor.execute('SELECT DISTINCT category FROM questions')
    return [row[0] for row in cursor.fetchall()]

def get_questions(category):
    cursor.execute('SELECT * FROM questions WHERE category=?', (category,))
    return cursor.fetchall()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Quiz Game')
        self.root.geometry('500x500')
        self.categories = get_categories()
        self.current_question = 0
        self.score = 0
        self.selected_category = tk.StringVar()
        self.questions = []
        self.start_time = None
        self.student_name = tk.StringVar()
        self.reg_no = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.header_label = tk.Label(self.root, text='Quiz Game', font=('Times New Roman', 32, 'bold'), fg='#2e86c1')
        self.header_label.pack(pady=(15, 5))
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)
        tk.Label(info_frame, text='Name:', font=('Arial', 12)).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(info_frame, textvariable=self.student_name, width=25, font=('Arial', 12)).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(info_frame, text='Registration No.:', font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        tk.Entry(info_frame, textvariable=self.reg_no, width=25, font=('Arial', 12)).grid(row=1, column=1, padx=5, pady=5)
        self.category_label = tk.Label(self.root, text='Select Category:', font=('Arial', 12, 'bold'))
        self.category_label.pack(pady=10)
        self.category_combo = ttk.Combobox(self.root, values=self.categories, textvariable=self.selected_category, state='readonly', font=('Arial', 12))
        self.category_combo.pack(pady=5)
        self.start_btn = tk.Button(self.root, text='Start Quiz', command=self.start_quiz, font=('Arial', 12, 'bold'), bg='#aed6f1')
        self.start_btn.pack(pady=10)
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)
        self.result_label = tk.Label(self.root, text='', font=('Arial', 12, 'bold'))
        self.result_label.pack(pady=10)

    def start_quiz(self):
        name = self.student_name.get().strip()
        reg = self.reg_no.get().strip()
        if not name or not reg:
            messagebox.showwarning('Warning', 'Please enter your name and registration number!')
            return
        category = self.selected_category.get()
        if not category:
            messagebox.showwarning('Warning', 'Please select a category!')
            return
        all_questions = get_questions(category)
        if not all_questions:
            messagebox.showinfo('Info', 'No questions found for this category.')
            return
        # Limit to 10 questions (randomly select if more than 10)
        if len(all_questions) > 10:
            self.questions = random.sample(all_questions, 10)
        else:
            self.questions = all_questions
        self.current_question = 0
        self.score = 0
        self.result_label.config(text='')
        self.show_question()

    def show_question(self):
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        if self.current_question >= len(self.questions):
            self.show_result()
            return
        row = self.questions[self.current_question]
        q_label = tk.Label(self.question_frame, text=row[2], wraplength=400, font=('Arial', 14, 'bold'))
        q_label.pack(pady=(10, 15))
        self.var = tk.IntVar()
        for i in range(4):
            opt = tk.Radiobutton(
                self.question_frame,
                text=row[3+i],
                variable=self.var,
                value=i+1,
                font=('Arial', 13),
                indicatoron=0,
                width=30,
                padx=10,
                pady=8,
                bg='#f2f4f4',
                selectcolor='#aed6f1',
                anchor='w',
                relief='ridge',
                bd=2
            )
            opt.pack(fill='x', pady=4, padx=10)
        hint_btn = tk.Button(self.question_frame, text='Show Hint', command=lambda: messagebox.showinfo('Hint', row[8] or 'No hint available.'), font=('Arial', 11), bg='#d5f5e3')
        hint_btn.pack(pady=8)
        submit_btn = tk.Button(self.question_frame, text='Submit', command=self.check_answer, font=('Arial', 12, 'bold'), bg='#aed6f1')
        submit_btn.pack(pady=8)
        self.start_time = time.time()

    def check_answer(self):
        elapsed = time.time() - self.start_time
        if elapsed > 10:
            messagebox.showinfo('Time\'s up!', 'You took too long! Moving to next question.')
            self.current_question += 1
            self.show_question()
            return
        answer = self.var.get()
        correct = self.questions[self.current_question][7]
        if answer == correct:
            self.score += 1
            messagebox.showinfo('Correct!', 'That\'s correct!')
        else:
            hint = self.questions[self.current_question][8] or 'No hint available.'
            messagebox.showinfo('Wrong!', f'Wrong answer! Hint: {hint}')
        self.current_question += 1
        self.show_question()

    def show_result(self):
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        name = self.student_name.get().strip()
        reg = self.reg_no.get().strip()
        self.result_label.config(text=f'Name: {name}\nReg. No.: {reg}\nYour final score is: {self.score}/{len(self.questions)}')
        restart_btn = tk.Button(self.question_frame, text='Restart', command=self.restart)
        restart_btn.pack(pady=10)

    def restart(self):
        self.result_label.config(text='')
        self.current_question = 0
        self.score = 0
        self.category_combo.set('')
        for widget in self.question_frame.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()