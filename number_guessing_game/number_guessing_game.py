import os
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Any


class Game:
    _SAVE_PATH: Path = Path(__file__).parent / 'score.json'
    _DIFFICULTY_OPTIONS: Dict[int, List[Any]] = {
        1: ["Easy", 10],
        2: ["Medium", 5],
        3: ["Hard", 3]
    }

    _difficulty: int = 0
    _guesses: int = 0
    _finished: bool = False

    def _create_save_file(self) -> None:
        if not os.path.exists(self._SAVE_PATH) or os.stat(self._SAVE_PATH).st_size <= 38:
            save_structure: Dict[str, str] = {
                "1": "0",
                "2": "0",
                "3": "0"
            }

            with open(self._SAVE_PATH, "w+") as f:
                json.dump(save_structure, f, indent=4)

    def _open_save(self) -> Dict[str, str]:
        with open(self._SAVE_PATH, "r") as f:
            data = json.load(f)
            return data

    def _save_score(self, difficulty: int, score: int) -> None:
        data = self._open_save()
        data.update({str(difficulty): str(score)})
        with open(self._SAVE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def _get_score(self, difficulty: int) -> int:
        return self._open_save().get(str(difficulty))

    def _input_difficulty(self) -> int:
        try:
            difficulty = int(input("Choose difficulty: "))
            return difficulty
        except ValueError:
            print("Value must be a number!")

    def _choose_difficulty(self) -> int:
        difficulty = self._input_difficulty()

        while difficulty not in self._DIFFICULTY_OPTIONS:
            print("There is no such difficulty option.")
            try:
                difficulty = self._input_difficulty()
            except ValueError:
                print("Value must be a number!")
        
        self._difficulty = difficulty
        self._guesses = self._DIFFICULTY_OPTIONS.get(difficulty)[1]

        return difficulty

    def _prepare_game(self) -> None:
        print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.\nYou have 5 chances to guess the correct number.\n")
        
        score_easy = "Not attempted" if (score_easy := int(self._get_score(1))) == 0 else score_easy
        score_medium = "Not attempted" if (score_medium := int(self._get_score(2))) == 0 else score_medium
        score_hard = "Not attempted" if (score_hard := int(self._get_score(3))) == 0 else score_hard

        print(f"Current highscores:\nEasy: {score_easy}\nMedium: {score_medium}\nHard: {score_hard}\n")
        
        print("Please select the difficulty level:\n1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances)\n")

        difficulty = self._choose_difficulty()

        print(f"\nGreat! You have selected the {self._DIFFICULTY_OPTIONS.get(difficulty)[0]} difficulty level.")
        print("Let's start the game!\n")

    def _game(self) -> None:
        start = time.time()
        number = random.randint(1, 100)
        for attempt in range(self._guesses):
            guess = int(input("Enter your guess: "))
            if guess > number:
                print(f"Incorrect! The number is less than {guess}.")
            elif guess < number:
                print(f"Incorrect! The number is greater than {guess}.")
            else:
                print(f"Congratulations! You guessed the correct number in {attempt} attempts.\n")
                print(f"You took {round(time.time() - start, 2)} seconds to guess.\n")
                if int(self._get_score(self._difficulty)) < attempt:
                    print(f"New highscore for {self._DIFFICULTY_OPTIONS.get(self._difficulty)[0]} difficulty!")
                    self._save_score(self._difficulty, attempt)
                self._finished = True
                return
        
        print(f"You did not manage to guess, the number was: {number}")
        print(f"Your attempt took {round(time.time() - start, 2)} seconds.\n")
        self._finished = True

    def game_controller(self) -> None:
        while True:
            if not self._finished:
                self._prepare_game()
                self._game()
            else:
                continue_playing = str(input("Would you like to continue playing? [y/n]: ")).lower().strip()
                if continue_playing == "y":
                    self._finished = False
                    self._choose_difficulty()
                    self._game()
                elif continue_playing == "n":
                    print("Thanks for playing!")
                    break

if __name__ == "__main__":
    game = Game()
    game.game_controller()
