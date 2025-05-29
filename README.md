# StaxTech

✅** Task 1: Currency Converter**

**Overview:**
This is a graphical currency converter app using Tkinter that allows users to convert between different currencies. It fetches real-time exchange rates from an online API and includes features such as dark mode toggle, swap currencies, conversion history, and offline support via caching.

**Code Explanation:**

CurrencyConverter class:

Handles the logic for fetching and caching currency rates.

Converts between currencies using the fetched exchange rates.

Falls back to a cached JSON file if there's no internet.

**Key methods:**

load_rates(base): Fetches exchange rates from the internet or local cache.

convert(amount, from_currency, to_currency): Performs currency conversion.

cache_rates(data): Saves rates locally for offline use.

CurrencyConverterApp class:

Creates the GUI using Tkinter.

Includes dropdowns for currency selection, entry for amount, buttons for conversion, theme toggle, and clear history.

**Key features:**

Conversion UI: Takes amount, from and to currency, and converts.

Swap Button: Swaps selected currencies.

Theme Toggle: Switches between light and dark mode.

History: Shows past conversions.

Real-time Rate Display: Shows conversion rate.

**main Function:**

Initializes the GUI window and starts the Tkinter main loop.

**Example Usage:**

User enters: Amount = 10, From = USD, To = INR.

Clicks convert.

Output: 10 USD = 834.23 INR.

![image](https://github.com/user-attachments/assets/e96ce781-1cf1-4171-b47a-915572f85859)



# StaxTech

✅** Task 2: Quiz Game**

**Overview:**
This is a GUI-based quiz game where students can input their name and registration number, choose a category, and answer timed multiple-choice questions from a SQLite database. It supports hints and displays the final score.

**Code Explanation:**

Database Setup:

Creates a questions table in SQLite (if not already present).

Prepopulates it with categories like Algorithms, Databases, OS, etc.

**insert_questions Function:**

Adds questions only if not already present in the database.

get_categories() and get_questions(category) Functions:

Fetch categories and questions from the database.

**QuizApp class:**
Handles the full quiz flow using Tkinter:

**Key features:**

Student Info Input: Takes name and registration number.

Category Selection: Dropdown to choose from available topics.

Randomized Questions: Selects 10 questions per session.

Timer: Limits answer time to 10 seconds.

Hint Button: Displays hint for each question.

Score Display: Shows score and result at the end.

Restart Option: User can restart the quiz after completion.

**main Function:**

Starts the Tkinter quiz interface.

**Example Usage:**

Name: Rushi, Reg. No.: AU129.

Category: Databases.

Question: "Which command removes all records from a table?"

User answers: TRUNCATE.

Output: Correct!

Final Score: 8/10.

![image](https://github.com/user-attachments/assets/96826e43-1fa9-4dfb-a1de-4a8d6bff24d7)


