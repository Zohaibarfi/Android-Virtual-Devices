import pyperclip

def set_clipboard_text(text):
    pyperclip.copy(text)
    print("Text has been set into the clipboard.")

if __name__ == "__main__":
    text_to_set = input("Enter the text to set into the clipboard: ")
    set_clipboard_text(text_to_set)
