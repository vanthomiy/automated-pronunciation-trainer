import pickle
import os
import random
from typing import Tuple, Any

import Levenshtein
from jiwer import wer


class UserHandler:
    def __init__(self, user_name):
        self.user_name = user_name
        self.history = []
        self.user_level = 0
        self.user_score = 0
        self.levels = ["a1", "a2", "b1", "b2", "c1", "c2", "native"]
        self.texts = self.load_texts()
        self.real_text = None

    def create_user_json(self):
        """
        create user json
        :return:
        """
        user = {
            "user_level": self.user_level,
            "user_score": self.user_score
        }

        return user

    def load_texts(self) -> dict:
        """
        load texts from sentences_{level}.txt
        :return:
        """
        texts = {}

        for i in range(len(self.levels)):
            level = self.levels[i]
            with open(f"./sentences/sentences_{level}.txt", "r") as f:
                texts[i] = f.readlines()

        return texts

    def get_text(self):
        """
        get random text from texts which is not in history
        :return:
        """
        # get random text from texts
        text = self.texts[self.user_level][random.randint(0, len(self.texts[self.user_level]) - 1)]

        # check if text is in history
        for history in self.history:
            if history["real_text"] == text:
                # get new text
                return self.get_text()

        self.real_text = text
        # return text
        return text

    def add_history(self, spoken_text) -> tuple[int, Any]:
        """
        add text to history and calculate wer and update user_score
        :param real_text:
        :param spoken_text:
        :return:
        """
        if self.real_text is None:
            return -1

        # calculate score (0-100) based on wer
        score = 100 - int(wer(self.real_text, spoken_text) * 100)

        if score < 0:
            score = 0
        self.user_score, count = self.calculate_user_score(score)
        sentence_alignment = self.mark_words_insert_delete_substitution(self.real_text, spoken_text)

        # add text to history
        self.history.append({
            "real_text": self.real_text,
            "spoken_text": sentence_alignment,
            "user_level": self.user_level,
            "user_score": self.user_score,
            "sentence_score": score
        })

        # update user level
        if count >= 5:
            if self.user_score > 80:
                self.user_level += 1
            elif self.user_score < 60:
                self.user_level -= 1

            # check if user level is in range
            if self.user_level < 0:
                self.user_level = 0
            elif self.user_level > 6:
                self.user_level = 6

        # save user
        self.save()

        return score, sentence_alignment

    def calculate_user_score(self, score) -> Tuple[int, int]:
        """
        Calculate user score based on last 1-5 scores from same level
        The score should be between 0 and 100
        :return:
        """
        # get the actual level
        level = self.user_level

        # get the directly last 4 scores and filter out the scores from other levels
        # get the last 4 histories from history
        last_history = self.history[-4:]

        # filter out the scores from other levels
        last_scores = [history["sentence_score"] for history in last_history if history["user_level"] == level]

        # sum up the scores
        sum_scores = sum(last_scores)

        # add the actual score
        sum_scores += score

        # divide the score by the max count of scores (5) as int
        user_score = sum_scores // 5

        # return the user score
        return user_score, len(last_scores) + 1

    def mark_words_insert_delete_substitution(self, real_text, spoken_text):
        """
            mark words in real text with insert, delete or substitution
            :param real_text:
            :param spoken_text:
            :return:
            """
        # to lower case
        real_text = real_text.lower()
        spoken_text = spoken_text.lower()

        # remove first " " if it exists in spoken text
        if spoken_text[0] == " ":
            spoken_text = spoken_text[1:]

        # remove all chars which are not letters or spaces
        real_text = "".join([char for char in real_text if char.isalpha() or char == " "])
        spoken_text = "".join([char for char in spoken_text if char.isalpha() or char == " "])

        list_to_remove = ["\n", "\t", "\r", "\""]

        # also remove all chars which are in list_to_remove
        for char in list_to_remove:
            real_text = real_text.replace(char, "")
            spoken_text = spoken_text.replace(char, "")

        # get real text words
        real_text_words = real_text.split(" ")

        # get spoken text words
        spoken_text_words = spoken_text.split(" ")

        # create corpus of all words in real text and spoken text (without duplicates)
        corpus = list(set(real_text_words + spoken_text_words))

        # each word in corpus gets a corresponding char
        corpus_index = {}
        for i in range(0, len(corpus)):
            corpus_index[corpus[i]] = chr(i + 97)

        # create text by corpus index
        real_text_index = ""
        for word in real_text_words:
            real_text_index += str((corpus_index[word]))

        spoken_text_index = ""
        for word in spoken_text_words:
            spoken_text_index += str((corpus_index[word]))

        # calculate alignment using Levenshtein (insert, delete, substitution, correct)

        alignment = Levenshtein.editops(spoken_text_index, real_text_index)

        # create return string
        return_alignment = ""
        for i in range(0, len(spoken_text_words)):
            # get alignment if i is in x[1] of alignment
            align = [x for x in alignment if x[1] == i]

            # if alignment is not empty
            if align:
                for a in align:
                    if a[0] == "insert":
                        return_alignment += f" <ins>{real_text_words[a[2]]}</ins>"
                        if len(a) == 1:
                            return_alignment += f" {spoken_text_words[a[1]]}"
                    # check if word is deleted
                    elif a[0] == "delete":
                        return_alignment += f" <del>{spoken_text_words[a[1]]}</del>"
                    # check if word is substituted
                    elif a[0] == "replace":
                        return_alignment += f" <mark>{spoken_text_words[a[1]]}</mark>"
            else:
                return_alignment += f" {spoken_text_words[i]}"

        return return_alignment

    def save(self):
        pickle.dump(self, open(f"users/{self.user_name}.pickle", "wb"))

    @staticmethod
    def get_user(user_name="user"):
        """
        load user from pickle file or create new user
        :return:
        """

        if os.path.exists(f"users/{user_name}.pickle"):
            return pickle.load(open(f"users/{user_name}.pickle", "rb"))
        else:
            return UserHandler(user_name)





