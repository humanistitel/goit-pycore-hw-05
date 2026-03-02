def input_error(func):
    """Decorator that handles input errors for handler functions."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"Contact {e} not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner


def parse_input(user_input):
    """Parse user input into a command and its arguments."""
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args, contacts):
    """Add a new contact to the contacts dictionary."""
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """Update an existing contact's phone number."""
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """Show the phone number for a given contact name."""
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts):
    """Return all contacts as a formatted string."""
    if not contacts:
        return "No contacts saved."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    handlers = {
        "add": lambda: add_contact(args, contacts),
        "change": lambda: change_contact(args, contacts),
        "phone": lambda: show_phone(args, contacts),
        "all": lambda: show_all(contacts),
        "hello": lambda: "How can I help you?",
    }

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        handler = handlers.get(command)
        print(handler() if handler else "Invalid command.")


if __name__ == "__main__":
    main()