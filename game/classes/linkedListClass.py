class Node:
    def __init__(self, data=None):
        self.data = data
        self.nextItem = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        node = Node(data)
        node.nextItem = self.head
        self.head = node

    def remove(self, data):
        currentItem = self.head
        prevItem = None
        while currentItem:
            if currentItem == data:
                if prevItem:
                    prevItem.nextItem = currentItem.nextItem
                else:
                    self.head = currentItem.nextItem
                return
            prevItem = currentItem
            currentItem = currentItem.nextItem

    def iterate(self):
        while self.head:
            yield self.head.data
            self.head = self.head.nextItem