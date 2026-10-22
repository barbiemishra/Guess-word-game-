from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "guess-the-word-secret"

words = ["python", "apple", "biryani", "barbie"]

hints = {
    "python": "A popular programming language 🐍",
    "apple": "A fruit that can be red or green 🍎",
    "biryani": "A flavorful rice dish 🍚",
    "barbie": "A famous fashion doll 🎀"
}


def start_game():
    word = random.choice(words)
    session["word"] = word
    session["charlist"] = list(word)
    session["attempts"] = len(word)
    session["guessed_letters"] = []
    session["chance"] = 0
    session["display"] = ["_"] * len(word)
    session["message"] = "GUESS THE WORD!"


@app.route("/", methods=["GET", "POST"])
def home():
    if "word" not in session:
        start_game()

    if request.method == "POST":
        if request.form.get("action") == "restart":
            start_game()
        else:
            a = request.form.get("letter", "").lower()

            if len(a) != 1 or not a.isalpha():
                session["message"] = "Enter only one letter!"

            elif a in session["guessed_letters"]:
                session["message"] = (
                    "The letter has been guessed buddy! "
                    "Try something else."
                )

            elif session["attempts"] > 0:
                session["guessed_letters"].append(a)
                count = 0

                for i in range(len(session["charlist"])):
                    if (
                        session["charlist"][i] == a
                        and session["display"][i] == "_"
                    ):
                        session["display"][i] = a
                        count += 1

                if count >= 1:
                    session["message"] = "Yeah, correct answer!"
                else:
                    session["message"] = "Wrong answer!"
                    session["chance"] += 1
                    session["attempts"] -= 1

                if session["display"].count("_") == 0:
                    session["message"] = (
                        "Hurray! You guessed the entire word!"
                    )
                elif session["attempts"] == 0:
                    session["message"] = (
                        "GAME OVER! The word was: " + session["word"]
                    )

    return render_template(
        "index.html",
        display=session["display"],
        attempts=session["attempts"],
        chance=session["chance"],
        guessed_letters=session["guessed_letters"],
        hint=hints[session["word"]],
        message=session["message"],
        game_over=(
            session["display"].count("_") == 0
            or session["attempts"] == 0
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)
