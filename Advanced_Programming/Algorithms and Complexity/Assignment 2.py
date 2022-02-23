from timeit import default_timer as timer
from collections import deque
from sortarray import *
# from FreqLinkedList import FreqLinkedList
import time

sorted_word_list = []
to_search_for_words = []

sorted_word_dict = {}

to_search_for_deque_list = deque([])
sorted_word_queue_list = deque([])

with open('C:/Users/Kris/Desktop/Uppsala HLT/Second Semester Modules/Advanced Programming/Algorithms and '
          'complexity/sortedWordList.txt', 'r') as f1:
    for index, line in enumerate(f1):
        line = line.strip()
        sorted_word_list.append(line)
        sorted_word_dict[line] = index
        sorted_word_queue_list.append(line)

with open('C:/Users/Kris/Desktop/Uppsala HLT/Second Semester Modules/Advanced Programming/Algorithms and '
          'complexity/toSearchFor.txt', 'r') as f2:
    for line in f2:
        line = line.strip()
        to_search_for_words.append(line)
        to_search_for_deque_list.append(line)

# SEARCHING!

# QUESTION 1:

# using indexing - to test on keys.txt


def sequential_search1(sorted_lst, word):
    for i in range(len(sorted_lst)):
        if word == sorted_lst[i]:
            return i
    return - 1


# using iterator (enumerate) - to test on keys.txt


def sequential_search2(sorted_lst, word):
    for i, w in enumerate(sorted_lst):
        if w == word:
            return i
    return -1

# sequential searches


def test_sequential1(sorted_lst, to_search_for):
    start = timer()
    for word in to_search_for:
        print(str(sequential_search1(sorted_lst, word)))
    end = timer()
    print(end - start)


def test_sequential2(sorted_lst, to_search_for):
    start = timer()
    for word in to_search_for:
        print(str(sequential_search2(sorted_lst, word)))
    end = timer()
    print(end - start)

# testing:
# test_sequential1(to_search_for_words) Time taken --> 62.922977641 seconds
# test_sequential2(to_search_for_words) Time taken --> 75.60868916 seconds


# binary search


def binary_search(lst, word):
    first = 0
    last = len(lst) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if lst[midpoint] == word:
            found = True
            return midpoint
        else:
            if word < lst[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    return -1


# print(binary_search(sorted_word_list, 'age'))


def test_binary(sorted_list, to_search_for):
    start = timer()
    for word in to_search_for:
        print(binary_search(sorted_list, word))
    end = timer()
    print(end - start)


# testing:
# test_binary(sorted_word_list, to_search_for_words) # 21.740182819 secs


# QUESTION 2:


def sequential_search_deque1(deque_lst, word):
    for i in range(len(deque_lst) - 1):
        if word == deque_lst[i]:
            return i
    return -1


def sequential_search_deque2(deque_lst, word):
    for i, w in enumerate(deque_lst):
        if w == word:
            return i
    return -1


def test_sequential_deque1(sorted_queue_lst, to_search_for_deque):
    start = timer()
    for word in to_search_for_deque:
        print(str(sequential_search_deque1(sorted_queue_lst, word)))
    end = timer()
    print(end - start)


def test_sequential_deque2(sorted_queue_lst, to_search_for_deque):
    start = timer()
    for word in to_search_for_deque:
        print(str(sequential_search_deque2(sorted_queue_lst, word)))
    end = timer()
    print(end - start)


# test_sequential_deque1(to_search_for_deque_list) # 444.483153906 secs
# test_sequential_deque2(to_search_for_words) # 125.443048485 secs


def binary_search_deque(deque_lst, word):
    first = 0
    last = len(deque_lst) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if deque_lst[midpoint] == word:
            found = True
            return midpoint
        else:
            if word < deque_lst[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    return -1


def test_binary_deque(to_search_for):
    start = timer()
    for word in to_search_for:
        print(binary_search_deque(sorted_word_queue_list, word))
    end = timer()
    print(end - start)


# test_binary_deque(to_search_for_words)  # 8.75 seconds!


# QUESTION 3:


def search_in_dict(sorted_dict, word):
    return sorted_dict.get(word, -1)

# print(search_in_dict(sorted_word_dict, 'age'))


def search_all_words_in_dict(alist):
    start = timer()
    for word in alist:
        print(search_in_dict(sorted_word_dict, word))
    end = timer()
    print("Time taken --> ", end - start)


# search_all_words_in_dict(to_search_for_words)  # 0.306747141 secs

# LINKED STRUCTURES

class Node:
    def __init__(self, data=None, freq=1):
        self.next = None
        self.data = data
        self.freq = freq


class FreqLinkedList:
    def __init__(self):
        self.head = Node()

    def addWord(self, word):
        if self.head.next == None:
            new_node = Node(word)
            self.head.next = new_node

        current = self.head
        previous = None

        while current.next:
            previous = current
            current = current.next
            if current.data == word:
                current.freq += 1
                return
            elif current.data > word:
                new_node = Node(word)
                previous.next = new_node
                new_node.next = current
                return
        if current.data == word:
            current.freq += 1
        elif current.data > word:
            new_node = Node(word)
            previous.next = new_node
            new_node.next = current
        else:
            current.next = Node(word)

    def filterWords(self, freq):
        while self.head is not None and self.head.freq < freq:
            self.head = self.head.next

        current_node = self.head
        while current_node is not None and current_node.next is not None:
            if current_node.next.freq < freq:
                current_node.next = current_node.next.next
            else:
                current_node = current_node.next

        return self.head

    def printList(self):
        current_node = self.head
        display_list = []
        while current_node:
            display_list.append((current_node.data, str(current_node.freq)))
            current_node = current_node.next
        for word_and_freq in display_list:
            if word_and_freq[0] is not None:
                word_and_freq = ' '.join(word_and_freq)
                print(word_and_freq)

# Testing:

# freqList = FreqLinkedList()
#
# with open("text.txt") as f:
#     for line in f:
#         words = line.split()
#         for word in words:
#             freqList.addWord(word)
#
# freqList.filterWords(50)
# freqList.printList()

# SORTING:


def selection_sort(sa):
    for i in range(0, sa.getSize() - 1):
        min = i
        for j in range(i + 1, sa.getSize()):
            if sa.cmp(j, min) < 0:
                min = j
        sa.swap(i, min)


def bubble_sort(sa):
    exchange = True
    num_to_pass = sa.getSize() - 1
    while num_to_pass > 0 and exchange:
        exchange = False
        for x in range(num_to_pass):
            if sa.cmp(x, x + 1) > 0:
                exchange = True
                sa.swap(x, x + 1)
    num_to_pass -= 1


def shell_sort(alist):
    array_size = alist.getSize()
    gap = int(array_size // 2)

    while gap > 0:
        for i in range(gap, array_size):
            j = i  # position
            while j >= gap and alist.cmp(j - gap, j) > 0:
                alist.swap(j, j - gap)
                j -= gap
        gap = int(gap // 2)


# debug = True

# test = SortArray()
#
# print("#######################")
# print("TESTING SELECTION SORT!")
# print()
#
# timer1_start = timer()
# for size in range(10, 51, 20):
#     print("SIZE: ", size)
#
#     for method in ["shuffle", "miniShuffle", "reverse"]:
#         print("METHOD: ", method)
#
#         test.reset(size, method)
#
#         if debug:
#             print("before: ")
#             test.printList()
#             print()
#
#         selection_sort(test)
#
#         if debug:
#             print("after: ")
#             test.printList()
#             print()
#
#         test.printInfo()
#
#     print()
# timer1_end = timer()
#
# print("#######################")
# print("TESTING BUBBLE SORT!")
# print()
#
# timer2_start = timer()
# for size in range(10, 51, 20):
#     print("SIZE: ", size)
#
#     for method in ["shuffle", "miniShuffle", "reverse"]:
#         print("METHOD: ", method)
#
#         test.reset(size, method)
#
#         if debug:
#             print("before: ")
#             test.printList()
#             print()
#
#         bubble_sort(test)
#
#         if debug:
#             print("after: ")
#             test.printList()
#             print()
#
#         test.printInfo()
#
#     print()
# timer2_end = timer()
#
# print("#######################")
# print("TESTING SHELL SORT!")
# print()
#
# timer3_start = timer()
# for size in range(10, 51, 20):
#     # changing_timer_start = timer()
#     print("SIZE: ", size)
#
#     for method in ["shuffle", "miniShuffle", "reverse"]:
#         print("METHOD: ", method)
#
#         test.reset(size, method)
#
#         if debug:
#             print("before: ")
#             test.printList()
#             print()
#
#         shell_sort(test)
#
#         if debug:
#             print("after: ")
#             test.printList()
#             print()
#
#         test.printInfo()
#     # changing_timer_end = timer()
#     # print("Size: ", size, "took ", changing_timer_end - changing_timer_start)
#     print()
# timer3_end = timer()
#
# print("Selection sort took--> ", timer1_end - timer1_start)
# print("Bubble sort took--> ", timer2_end - timer2_start)
# print("Shell sort took--> ", timer3_end - timer3_start)
