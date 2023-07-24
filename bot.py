from classes import AddressBook, Name, Phone, Record


address_book = AddressBook()


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input. Please enter a valid name and phone number"
        except IndexError:
            return "Invalid input. please try again"
    return wrapper


@handle_errors
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    address_book.add_record(rec)
    return "Contact added successfully."


@handle_errors
def greeting(*text):
    return "How can I help you?"


@handle_errors
def exit_command(*args):
    return "See you soon"


@handle_errors
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.edit_phone(old_phone, new_phone)

    return f"No contact {name} in addressbook."
@handle_errors
def phone(*args):
    search_items = ["l","i","b"]
    result = address_book.search_contact(search_items)
    if result == "Contact found":
        name = Name(args[0])
        if name in address_book[name]:
            contact = address_book[name]
            phones_str = ', '.join(str(phone) for phone in contact.phones)
            return f"Phone numbers for {name}: {phones_str}"
    return result


    

@handle_errors
def show_all(*args):
    search_items = ["l","i","b"]
    result = address_book.search_contact(search_items)
    if result == "Contact found":
        all_contacts = ""
        for record in address_book.values():
            all_contacts += f"{record.name}"
        return all_contacts
    else:
        return result



@handle_errors
def no_command(*args):
    return "Unknown command"


COMMANDS = {add: ("add",),
            change: ("change",),
            phone: ("phone",),
            show_all: ("show all",),
            greeting: ("hello", "hi"),
            exit_command: ("good bye", "exit")
            }


def parser(text: str) -> tuple[callable, tuple[str] | None]:
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data

    return no_command, []


def main():
    while True:
        user_input = input(">>>>")
        command, data = parser(user_input)
        result = command(*data)
        print(result)

        if command == exit_command:
            break


if __name__ == "__main__":
    main()
