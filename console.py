#!/usr/bin/python3
"""AirBnB Console Application"""

import cmd
import sys
import json
from models.engine import name_class
from models import storage
from models import City
from models import Place
from models import Review
from models import State
from models import Amenity
from models import BaseModel
from models import User


def parse_args(args):
    if args:
        all_args = args.split(' ')
        return all_args
    return


def complete_class_arg(text, line, begidx, endidx):
    if not text:
        completions = name_class[:]
    else:
        completions = [
            class_name
            for class_name in name_class
            if class_name.startswith(text)]
    return completions


class HBNBCommand(cmd.Cmd):
    """AirBnB Console APP Subclass
    """
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Exit CLI when `quit` is entered"""
        return True

    def do_EOF(self, arg):
        """Execute nothing for an EOF input"""
        return True

    def emptyline(self):
        """Execute nothing for an empty line command"""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel
        create: create <class_name> (ex: create BaseModel)
        """

        all_args = parse_args(args)

        if not all_args:
            print("** class name missing **")
            return
        elif all_args[0] not in name_class:
            print("** class doesn't exist **")
            return

        class_name = all_args[0]

        # create new BaseModel instance
        new_instance = eval(class_name)()

        # save to file.json
        storage.new(new_instance)
        storage.save()

        # print id
        print(new_instance.id)

    def complete_create(self, text, line, begidx, endidx):
        return complete_class_arg(text, line, begidx, endidx)

    def do_show(self, args):
        """Prints the string representation of an instance based\
                on the class name and id
        show: show <class_name> <instance id>
        """

        all_args = parse_args(args)

        if not all_args:
            print("** class name missing **")
            return
        elif all_args[0] not in name_class:
            print("** class doesn't exist **")
            return
        elif len(all_args) < 2:
            print("** instance id missing **")
            return

        class_name = all_args[0]
        inst_id = all_args[1]

        # print string rep of an instance base on class name and id
        obj_key = f'{class_name}.{inst_id}'

        storage.reload()
        objs_in_dict = storage.all()

        try:
            obj = objs_in_dict[obj_key]
        except:
            print('** no instance found **')
        else:
            print(obj)

    def complete_show(self, text, line, begidx, endidx):
        return complete_class_arg(text, line, begidx, endidx)

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id
        destroy: destroy <class_name> <instance id>
        """

        all_args = parse_args(args)

        if not all_args:
            print("** class name missing **")
            return
        elif all_args[0] not in name_class:
            print("** class doesn't exist **")
            return
        elif len(all_args) < 2:
            print("** instance id missing **")
            return

        class_name = all_args[0]
        inst_id = all_args[1]

        obj_key = f'{class_name}.{inst_id}'

        storage.reload()
        objs_in_dict = storage.all()

        try:
            del objs_in_dict[obj_key]
        except:
            print('** no instance found **')
        else:
            storage.save()

    def complete_destroy(self, text, line, begidx, endidx):
        return complete_class_arg(text, line, begidx, endidx)

    def do_all(self, args):
        """Prints all string representation of all instances
        all: all [<class_name>]
        """

        all_args = parse_args(args)

        if all_args and all_args[0] not in name_class:
            print("** class doesn't exist **")
            return

        storage.reload()
        objs_in_dict = storage.all()
        objs_list = []

        # return all objs if class name is not specified.
        try:
            class_name = all_args[0]
        except:
            for obj in objs_in_dict.values():
                objs_list.append(obj.__str__())
        else:
            # give objs with the specified class name if class name is given
            for obj in objs_in_dict.values():
                if class_name == obj.__class__.__name__:
                    objs_list.append(obj.__str__())

        print(objs_list)

    def complete_all(self, text, line, begidx, endidx):
        return complete_class_arg(text, line, begidx, endidx)

    def do_update(self, args):
        """Updates an instance based on the class name and id
        update: update <class_name> <instance id> <attribute name>
        "<attribute value>"
        """

        all_args = parse_args(args)

        if not all_args:
            print("** class name missing **")
            return
        elif all_args[0] not in name_class:
            print("** class doesn't exist **")
            return
        elif len(all_args) < 2:
            print("** instance id missing **")
            return

        class_name = all_args[0]
        inst_id = all_args[1]

        obj_key = f'{class_name}.{inst_id}'

        storage.reload()
        objs_in_dict = storage.all()

        try:
            obj = objs_in_dict[obj_key]
        except:
            print('** no instance found **')
            return

        try:
            attr_name = all_args[2]
        except:
            print("** attribute name missing **")
            return

        try:
            attr_value = all_args[3]
            obj_attr = obj.__dict__[attr_name]
        except KeyError:  # if attr_name(key) not in obj, add it to the object
            obj.__dict__.update({attr_name: attr_value})
            storage.save()
            return
        except:
            print("** value missing **")
            return
        else:
            obj.__dict__[attr_name] = attr_value
            storage.save()

    def complete_update(self, text, line, begidx, endidx):
        return complete_class_arg(text, line, begidx, endidx)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
