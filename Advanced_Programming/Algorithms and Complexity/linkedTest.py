from FreqLinkedList import FreqLinkedList

freqList = FreqLinkedList()

with open ("text.txt") as f:
    for line in f:
        words = line.split()
        for word in words:
            freqList.addWord(word)

freqList.filterWords(50)
freqList.printList()
