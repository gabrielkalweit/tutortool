import sys
import getpass
import multiSVN as msvn
import eclipse_importer as ei
import feedback_creator as fc
import tutortool_config as ttc
import infocolor as ic


class TutorTool:
    def print_usage(self):
        print("tutortool.py <command> [last_monday, -m \"commit_message\", exNN_N*]")
        print("commands: add, addci, checkout, commit, create, import, refresh, revert, update")
        print("")
        print("alternative: tutortool.py <exNN_N*>")
        print("leads to: update last_monday create import exNN_N*")

    def __init__(self):
        self.config = ttc.TutorToolConfig()
        self.active_commands = []
        self.commit_message = ""
        self.ex_list = []
        self.last_monday = False
        self.svn_commands = ["add", "addci", "checkout", "commit", "refresh", "revert", "update"]
        self.commands = self.svn_commands[:] + ["create", "import"]
        self.password = ""
        self.username = ""

    def process_arguments(self, argv):
        if len(argv) <= 1:
            self.print_usage()
            exit()

        i = 1
        while (i < len(argv)):
            if argv[i] in self.commands:
                self.active_commands.append(argv[i])
            elif argv[i].startswith("ex"):
                self.ex_list.append(argv[i])
            elif argv[i] == "last_monday":
                self.last_monday = True
            elif argv[i] == "-m" and i < len(argv) - 1:
                self.commit_message = argv[i + 1]
                i += 1
            else:
                ic.Info.printe("Invalid command.")
                self.print_usage()
                exit()
            i += 1

        if self.ex_list and not self.active_commands:
            self.last_monday = True
            self.active_commands.append("update")
            self.active_commands.append("create")
            self.active_commands.append("import")

        for command in self.active_commands:
            if command in self.svn_commands:
                self.username = input("User: ")
                self.password = getpass.getpass("Password: ")
            if (command == "commit" or command == "addci") and not self.commit_message:
                self.commit_message = input("Commit Message: ")

    def run(self):
        for command in self.active_commands:
            ic.Info.prints("Start with " + command)
            if command in self.svn_commands:
                client = msvn.MultiSVN(self.config, self.username, self.password)
                if command == "add":
                    client.add()
                elif command == "addci":
                    client.addci(self.commit_message)
                elif command == "checkout":
                    client.checkout()
                elif command == "commit":
                    client.commit(self.commit_message)
                elif command == "refresh":
                    client.clean()
                    client.checkout(self.last_monday)
                elif command == "revert":
                    client.revert()
                elif command == "update":
                    client.update(self.last_monday)
            elif command == "create":
                client = fc.FeedBackCreator(self.config)
                client.create_feedback_files(self.ex_list)
            elif command == "import":
                client = ei.EclipseImporter(self.config)
                client.import_projects(self.ex_list)
            else:
                ic.Info.printe("Invalid command.")
                self.print_usage()
                exit()

            ic.Info.prints("Done with " + command)
        ic.Info.prints("Terminate")

tool = TutorTool()
tool.process_arguments(sys.argv)
tool.run()