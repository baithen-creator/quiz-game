def remove_articles(text):
    articles = ['the', 'a', 'an']
    words = text.split()
    return ' '.join([word for word in words if word not in articles])

def fuzzy_match(answer, correct, max_errors=2):
    if len(answer) != len(correct):
        return False
    errors = sum(1 for a, c in zip(answer, correct) if a != c)
    return errors <= max_errors

def check_answer(user_answer, correct_answer):
    user_clean = remove_articles(user_answer.lower().strip())
    correct_clean = remove_articles(correct_answer.lower())
    
    if user_clean == correct_clean:
        return True
    if correct_clean in user_clean:
        return True
    if user_clean in correct_clean:
        return True
    if not correct_clean.isdigit() and fuzzy_match(user_clean, correct_clean):
        return True
    return False

def load_questions(filename='questions.txt'):
    questions = []
    with open(filename, 'r') as file:
        for line in file:
            question, answer = line.strip().split('|')
            questions.append({"question": question, "answer": answer.lower()})
    return questions

def load_quiz_setup(setup_file='quiz_setup.txt'):
    rounds = []
    with open(setup_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                round_name, question_file = line.split('|')
                rounds.append({"name": round_name, "file": question_file})
    return rounds

def save_result(name, score):
    with open('results.txt', 'a') as file:
        file.write(f"{name}|{score}\n")

def show_leaderboard():
    try:
        with open('results.txt', 'r') as file:
            results = []
            for line in file:
                line = line.strip()
                if line:
                    name, score = line.split('|')
                    results.append((name, int(score)))
            
            if results:
                results.sort(key=lambda x: x[1], reverse=True)
                print("\n=== TOP 10 LEADERBOARD ===")
                for i, (name, score) in enumerate(results[:10], 1):
                    print(f"{i:2}. {name:<15} {score} points")
            else:
                print("\nNo previous results found.")
    except (FileNotFoundError, ValueError):
        print("\nNo previous results found.")

def run_single_round(round_name, question_file):
    questions = load_questions(question_file)
    score = 0
    
    print(f"\n=== {round_name.upper()} ===")
    print("(Type 'quit' at any time to exit)")
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        answer = input("Your answer: ").lower().strip()
        
        if answer == "quit":
            return None
        
        if check_answer(answer, q['answer']):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The answer was: {q['answer']}")
    
    print(f"\n{round_name} complete! Your score: {score}/{len(questions)}")
    return score

def run_multi_round_quiz(setup_file='quiz_setup.txt'):
    rounds = load_quiz_setup(setup_file)
    total_score = 0
    round_scores = []
    
    print("Welcome to the Multi-Round Quiz Game!")
    print("(Answers are checked with partial matching and typo tolerance)")
    name = input("Enter your name: ").strip()
    if not name:
        name = "Anonymous"
    
    show_leaderboard()
    print(f"\nGood luck, {name}! You have {len(rounds)} rounds to complete.")
    
    for round_info in rounds:
        score = run_single_round(round_info['name'], round_info['file'])
        if score is None:
            print("Thanks for playing!")
            return
        
        total_score += score
        round_scores.append((round_info['name'], score))
        input("\nPress Enter to continue to next round...")
    
    print(f"\n=== FINAL RESULTS ===")
    for round_name, score in round_scores:
        print(f"{round_name}: {score} points")
    print(f"TOTAL SCORE: {total_score} points")
    
    save_result(name, total_score)
    show_leaderboard()
    input("\nPress Enter to exit...")

def run_quiz(question_file='questions.txt'):
    questions = load_questions(question_file)
    score = 0
    
    print("Welcome to the Quiz Game!")
    print("(Answers are checked with partial matching and typo tolerance)")
    name = input("Enter your name: ").strip()
    if not name:
        name = "Anonymous"
    
    show_leaderboard()
    print(f"\nGood luck, {name}!")
    print("(Type 'quit' at any time to exit)")
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        answer = input("Your answer: ").lower().strip()
        
        if answer == "quit":
            print("Thanks for playing!")
            return
        
        if check_answer(answer, q['answer']):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The answer was: {q['answer']}")
    
    print(f"\nQuiz complete! Your score: {score}/{len(questions)}")
    save_result(name, score)
    show_leaderboard()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    import sys
    
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "--clear":
                open('results.txt', 'w').close()
                print("Results cleared! Starting fresh.\n")
                run_multi_round_quiz('quiz_setup.txt')
            elif sys.argv[1].endswith('.txt'):
                print(f"Using question file: {sys.argv[1]}\n")
                run_quiz(sys.argv[1])
        else:
            run_multi_round_quiz('quiz_setup.txt')
    
    except FileNotFoundError as e:
        if 'quiz_setup.txt' in str(e):
            print("Multi-round setup file 'quiz_setup.txt' not found.")
            print("To run single round, use: QuizGame.exe questions.txt")
        else:
            print("Error: Question file not found.")
            print("Make sure the file exists in the same directory as the game.")
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\nThanks for playing!")