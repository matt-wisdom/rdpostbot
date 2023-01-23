"""
    Tool to add, delete and show messages.
    Use 'poetry run meman' to run.
"""

import json
import imghdr
import pathlib

def multiline_input():
    lines = []
    spaces = 0
    while True:
        line = input()
        lines.append(line)
        if line:
            spaces = 0
        else:
            spaces += 1
        if spaces == 3:
            break
    return "\n\n".join(lines[:-3])

def get_yesno(question: str) -> bool:
    """
        Prompt user for yes or no response until
        they give valid input.
    """
    while True:
        choice = input(question + "(Y/N): ").lower() + " "
        if choice[0] not in ["y", "n"]:
            print("Invalid input. Select Y or N")
            continue
        return True if choice[0] == "y" else False

def input_noempty(prompt: str="") -> str:
    """
        Receive non empty input
    """
    inp = ""
    while not inp:
        inp = input(prompt)
    return inp

def add_new():
    messages_data = json.load(open("messages.json"))
    data = {}
    data["title"] = input_noempty("Post Title:")
    if get_yesno("Add body (text)?"):
        print("Input Post body (input 3 empty lines when done): ")
        data["body"] = multiline_input()
    else:
        if get_yesno("Add images?"):
            print("Input path to folder with the images.")
            images = []
            folder = input_noempty("Image Folder Path:")
            files = pathlib.Path(folder).iterdir()
            for file in files:
                if imghdr.what(file):
                    images.append(str(file.absolute()))
            data["images"] = images
    if get_yesno("Add flair?"):
        data["flair"] = input_noempty("Flair text:")
    if get_yesno("Add comments?"):
        data["comment"] = input_noempty("Comment text:")
    subs = input_noempty("Input subreddits, seperated by comma: ")
    data["subreddits"] = [sub.strip() for sub in subs.split(",")]
    data["interval"] = int(input_noempty("Interval btw messages in seconds: "))
    messages_data["messages"].append(data)
    with open("messages.json", "w") as f:
        json.dump(messages_data, f)
    print("Added")

def list_messages():
    messages_data = json.load(open("messages.json"))["messages"]
    for i, message in enumerate(messages_data):
        print("--------------------------------------")
        print(f"ID: {i+1}\n")
        print(f"TITLE: {message['title'][:50]}...\n")
        print(f"BODY: {message.get('body', '')[:50]}...\n")
        print(f"SUBREDDITS: {message['subreddits']}\n")
        print(f"FLAIR: {message.get('flair')}\n")
        print(f"IMAGES: {message.get('images', [])}\n")
        print(f"COMMENT: {message.get('comment', '')[:50]}...\n")
        print("--------------------------------------\n\n")

def delete_message():
    messages_data = json.load(open("messages.json"))
    id = int(input_noempty("Message ID: "))
    msg = messages_data["messages"].pop(id-1)
    with open("messages.json", "w") as f:
        json.dump(messages_data, f)
    print(f"Deleted {msg['title'][:20]}...")

def main():
    print(" Message Creator for reddit bot ".center(40, '-'))
    while True:
        prompt = "\n1. Add New Message\n2. List Messages\n3. Delete Message\nq. Exit\n\nChoice: "
        choice = input(prompt).lower()
        try:
            if choice == '1':
                add_new()
            elif choice == '2':
                list_messages()
            elif choice == '3':
                delete_message()
            elif choice == 'q':
                break
            else:
                print("Invalid choice")
                continue
        except Exception as e:
            print("Exiting....", e)

if __name__ == '__main__':
    main()