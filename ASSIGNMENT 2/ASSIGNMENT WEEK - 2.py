class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        
    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = new_node
    
    def print_list(self):
        current_node = self.head
        if not current_node:
            print("List is empty.")
            return
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")
        
    def del_node(self, n):
        if self.head is None:
            raise Exception("List is empty.")
        
        if n < 1:
            raise Exception("Index out of range")
        
        if n == 1:
            self.head = self.head.next
            return
        
        current_node = self.head
        for i in range(n - 2):
            if current_node.next is None:
                raise Exception("Index out of range")
            current_node = current_node.next
        
        if current_node.next is None:
            raise Exception("Index out of range")
        
        current_node.next = current_node.next.next


ll = LinkedList()

while True:
    print("\n--- Linked List Menu ---")
    print("1. Add Node")
    print("2. Delete Node at Position")
    print("3. Print Linked List")
    print("4. Exit")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        value = input("Enter value to add: ")
        ll.add_node(int(value))
        print("Node added.")
        
    elif choice == '2':
        position = input("Enter position to delete (1-based index): ")
        try:
            ll.del_node(int(position))
            print("Node deleted.")
        except Exception as e:
            print("Error:", e)
    
    elif choice == '3':
        print("Linked List:")
        ll.print_list()
    
    elif choice == '4':
        print("Exiting program.")
        break
    
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")