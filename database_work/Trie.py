import os
import pickle

__author__ = 'ava-katushka'


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = {}
        self.list = []

    def add_node(self, letter):
        new_node = Node(parent=self)
        self.dict[letter] = new_node
        return new_node

    def has_node(self, letter):
        return letter in self.dict

    def go_by_node(self, letter):
        if self.has_node(letter):
            return self.dict[letter]
        else:
            return self.add_node(letter)

    def get_list(self):
        return self.list

    def add_to_list(self, value):
        list.append(value)


class Trie:
    _SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))

    def __init__(self):
        self.file_name = os.path.join(Trie._SCRIPT_ROOT, "trie_dump.txt")
        if os.path.isfile(self.file_name):
            with open(self.file_name) as trie_file:
                self.root = pickle.load(trie_file)
        else:
            self.root = Node()

    def add_word(self, word, value):
        node = self.root
        for letter in word:
            node = node.go_by_node(letter)
        node.add_to_list(value)

    def find_exactly_word(self, word):
        node = self.root
        for letter in word:
            node = node.go_by_node(letter)
        return node.get_list()

    def save_trie(self):
        with open(self.file_name) as trie_file:
            pickle.dump(self.root, trie_file)
