from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact doesn't exist."
    return inner

def parse_input(user_input):
    """Split the input into a lowercase command and a list of arguments."""
    try:
        cmd, *args = user_input.split()
    except ValueError:  # empty input
        return "", []
    return cmd.lower(), args

@input_error
def add_contact(args, contacts):
    """Add a contact. 
    
    Format: add [name] [phone]
    """
    name, phone = args
    
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    """Change the phone of an existing contact.

    Format: change [name] [phone]
    """
    name, phone = args
    #makes the decorator return "Contact doesn't exist."
    if name not in contacts:
        raise KeyError(name)
    
    contacts[name] = phone
    return "Contact updated."

    
@input_error
def show_phone(args, contacts):
    """Return the phone of a contact.

    Format: phone [name]
    """
    name = args[0]
    return contacts[name]

@input_error
def show_all(contacts):
    """Returns all contacts

    Format: all
    """
    if not contacts:
        return "No contacts."
    
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()