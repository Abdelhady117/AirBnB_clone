#!/usr/bin/python3

""" The command interpreter for AirBnB project. """

import cmd
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Defines the command interpreter. """

    prompt = '(hbnb) '
    __models = {"BaseModel": BaseModel, "User": User, "State": State, "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """ EOF command (Ctrl + D) to exit the program. """
        print()
        return True

    def emptyline(self):
        """ emptyline + Enter shouldn't execute anything. """
        pass
    @staticmethod
    def do_clear(_):
        """ Cleans the console. """
        os.system("clear")

    def default(self, line):
        """Handle unrecognized commands."""
        print(f"** unknown command: {line.strip()} **\nType 'help' for available commands")

    def precmd(self, line):
        """ . """
        if '.' in line and '(' in line and ')' in line:
            class_name, rest = line.split('.', 1)
            method, args = rest.split('(', 1)
            method = method.strip()
            args = args.rstrip(')')
            if not args and method in ['all', 'count']:
                return f"{method} {class_name}"
            if ',' in args:
                uid, rest_args = args.split(',', 1)
            else:
                uid = args
            uid = uid.strip('"').strip()
            if method in ['show', 'destroy']:
                return f"{method} {class_name} {uid}"
            elif method == 'update':
                update_line = method + " " + class_name + " " + uid + " "
                try:
                    #if rest_args.strip().startswith('{') and rest_args.endswith('}'):
                    if '{' and '}' in rest_args:
                        rest_args = rest_args.replace("'", '"').strip()
                        update_line += rest_args
                    else:
                        rest_args = rest_args.replace('"', ' ').replace(',', ' ')
                        update_line += rest_args
                except:
                    pass
                return update_line
        else:
            return line

    def do_create(self, arg):
        """ Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id. """
        if not arg:
            print("** class name missing **")
            return
        try:
            new_inst = eval(arg.split()[0])()
            new_inst.save()
            print(new_inst.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """ Prints the string representation of an instance based on the class name and id. """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.__models:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if instance is None:
            print("** no instance found **")
        else:
            print(instance)

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id (save the change into the JSON file). """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.__models:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """ Prints all string representation of all instances based or not on the class name. """
        if not arg:
            all_instances = [str(obj) for obj in storage.all().values()]
            print(all_instances)
        elif arg not in self.__models:
            print("** class doesn't exist **")
        else:
            model_instances = [str(obj) for key, obj in storage.all().items() if key.startswith(arg + '.')]
            print(model_instances)

    def do_count(self, line):
        """
        Retrieve the number of instances of a class: <class name>.count()
        """
        if not line:
            print("** class name missing **")
        elif line not in self.__models:
            print("** class doesn't exist **")
        else:
            inst_count = 0
            for obj in storage.all().values():
                if obj.__class__.__name__ == line.strip():
                    inst_count += 1
            print(inst_count)

    def do_update(self, arg):
        """ update an instance based on $ update <class name> <id> <attribute name> "<attribute value>" Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file). """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.__models:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if instance is None:
            print("** no instance found **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif args[2].strip().startswith('{') and args[2].endswith('}'):
            try:
                # converts single quotes in the dictionary string to double quotes so
                # it can be processed as JSON
                j = args[2].replace("'", '"').strip()
                # convert string to dictionary
                attr_dict = json.loads(args[2])
            except json.JSONDecodeError:
                print("** invalid dictionary format **")
                return
            for attr_name, attr_value in attr_dict.items():
                parsed_line = args[0] + " " + args[1] + " " + attr_name + " " + attr_value
                self.do_update(parsed_line)
        elif args[2] in ["id", "created_at", "updated_at"]:
            print(f"{args[2]} can't be updated")
            return
        else:
            if args[2] in ["id", "created_at", "updated_at"]:
                print(f"** {args[2]} can't be updated **")
                return
            if len(args) == 3:
                print("** value missing **")
                return
            attr_name = args[2]
            attr_value = args[3].strip('"')
            try:
                if '.' in attr_value:
                    attr_value = float(attr_value)
                else:
                    attr_value = int(attr_value)
            except ValueError:
                pass
            setattr(instance, attr_name, attr_value)
        #storage.all()[key].save()
        instance.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
