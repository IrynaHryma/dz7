import classes


address_book = classes.AddressBook()


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
    name = classes.Name(args[0])
    phone = classes.Phone(args[1])
    birthday = classes.Birthday(args[2]) if len(args) > 2 else None
    address = classes.Address(
        street=args[3], city=args[4], country=args[5], zipcode=args[6])
    email = classes.Email(args[7])
    rec: classes.Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = classes.Record(name, phone, birthday, address, email)
    address_book.add_record(rec)
    return "Contact added successfully."


@handle_errors
def greeting(*text):
    return "How can I help you?"


# exit


@handle_errors
def exit_command(*args):
    return "See you soon"


@handle_errors
def change(*args):
    name = classes.Name(args[0])
    old_phone = classes.Phone(args[1])
    new_phone = classes.Phone(args[2])
    rec: classes.Record = address_book.get(str(name))
    if rec:
        return rec.edit_phone(old_phone, new_phone)

    return f"No contact {name} in addressbook."


@handle_errors
def phone(*args):
    name = classes.Name(args[0])
    if str(name) in address_book.data:
        contact = address_book.data[str(name)]
        phones_str = ', '.join(str(phone) for phone in contact.phones)
        return f"Phone numbers for {name}: {phones_str}"
    return "Contact not found"


@handle_errors
def find_command(*args):
    if len(args[0]) < 3:
        return "Enter at leaset three characters to seartch"
    return address_book.search_contact(args[0])


@handle_errors
def show_all(*args):
    return address_book


@handle_errors
def birthday_greeting(*args):
    name = classes.Name(args[0])
    rec: classes.Record = address_book.get(str(name))
    if rec:
        greeting = rec.days_to_birthday()
        if greeting:
            return greeting
        else:
            return f"No  birthday today for {name}"

    else:
        return f"No contact with name{name} found"


@handle_errors
def address(*args):
    name = classes.Name(args[0])
    rec: classes.Record = address_book.get(str(name))
    if rec:
        return f"Address  for {name}: {rec.address}."


@handle_errors
def email(*args):
    name = classes.Name(args[0])
    rec: classes.Record = address_book.get(str(name))
    if rec:
        return f"Email for {name}: {rec.email}"


@handle_errors
def no_command(*args):
    return "Unknown command"


COMMANDS = {add: ("add",),
            change: ("change",),
            phone: ("phone",),
            show_all: ("show all",),
            greeting: ("hello", "hi"),
            exit_command: ("finish", "exit", "end"),
            find_command: ('search', 'find',),
            birthday_greeting: ("birthday",),
            address: ("address",),
            email: ("email"),
            }


def parser(text: str) -> tuple[callable, tuple[str] | None]:
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data

    return no_command, []


def main():
    try:
        address_book.read_from_file("Address_book")

    except FileNotFoundError:
        print("File not found. Start the address_book")

    while True:
        user_input = input(">>>>")
        command, data = parser(user_input)
        result = command(*data)
        print(result)

        if command == exit_command:
            address_book.save_to_file("Address_book")
            break


if __name__ == "__main__":
    main()
