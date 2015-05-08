import configparser as cp
import os, ast, sys

# --- Constants ---
FILENAME = "config.cfg"
SECTIONNAME_SVN = "SVN"
SECTIONNAME_ECLIPSE = "Eclipse"
SECTIONNAME_FEEDBACK = "Feedback"
OPTIONNAME_SVN_SVNROOT = "svnroot"
OPTIONNAME_SVN_REPOS = "subrepos"
OPTIONNAME_SVN_LOCALTARGET = "local_target_dir"
OPTIONNAME_ECLIPSE_PROJECTS_LOCALTARGET = "project_local_target_dir"
OPTIONNAME_ECLIPSE_FILE_EXTENSIONS = "file_extensions"
OPTIONNAME_FEEDBACK_TEMPLATE = "feedback_template"

class TutorToolConfig:
    def __init__(self, debug=False):
        self.debug = debug
        self.options = {}

        if (self.existCfg()): self.parseCfg()
        else:
            print("Could not find configuration file.")

    def existCfg(self):
        return os.path.exists(FILENAME) and os.path.isfile(FILENAME)

    def parseCfg(self):
        if (self.debug): print("Parsing the configuration file...")
        self.parser = cp.ConfigParser()
        self.parser.readfp(open(FILENAME))

        # Parse and save the individual options
        self.options[OPTIONNAME_SVN_SVNROOT] = self.parser.get(SECTIONNAME_SVN, OPTIONNAME_SVN_SVNROOT)
        self.options[OPTIONNAME_SVN_REPOS] = [str(x).strip() for x in ast.literal_eval(self.parser.get(SECTIONNAME_SVN, OPTIONNAME_SVN_REPOS))]
        self.options[OPTIONNAME_SVN_LOCALTARGET] = self.parser.get(SECTIONNAME_SVN, OPTIONNAME_SVN_LOCALTARGET)
        self.options[OPTIONNAME_ECLIPSE_PROJECTS_LOCALTARGET] = self.parser.get(SECTIONNAME_ECLIPSE, OPTIONNAME_ECLIPSE_PROJECTS_LOCALTARGET)
        self.options[OPTIONNAME_FEEDBACK_TEMPLATE] = self.parser.get(SECTIONNAME_FEEDBACK, OPTIONNAME_FEEDBACK_TEMPLATE)
        self.options[OPTIONNAME_ECLIPSE_FILE_EXTENSIONS] = [str(x).strip() for x in ast.literal_eval(self.parser.get(SECTIONNAME_ECLIPSE, OPTIONNAME_ECLIPSE_FILE_EXTENSIONS))]

    def getSvnRoot(self):
        return self.options[OPTIONNAME_SVN_SVNROOT]

    def getSvnRepositories(self):
        return self.options[OPTIONNAME_SVN_REPOS]

    def getLocalTargetDir(self):
        return self.options[OPTIONNAME_SVN_LOCALTARGET]

    def getLocalEclipseTargetDir(self):
        return self.options[OPTIONNAME_ECLIPSE_PROJECTS_LOCALTARGET]

    def getFileExtensions(self):
        return self.options[OPTIONNAME_ECLIPSE_FILE_EXTENSIONS]

    def getFeedbackTemplate(self):
        return self.options[OPTIONNAME_FEEDBACK_TEMPLATE]

    def printConfiguration(self):
        print(OPTIONNAME_SVN_SVNROOT + ": " + self.getSvnRoot())
        print(OPTIONNAME_SVN_LOCALTARGET + ": " + self.getLocalTargetDir())
        print(OPTIONNAME_SVN_REPOS + ": [" + ", ".join(str(x) for x in self.getSvnRepositories()) + "]")
        print(OPTIONNAME_ECLIPSE_PROJECTS_LOCALTARGET + ": " + self.getLocalEclipseTargetDir())
        print(OPTIONNAME_ECLIPSE_FILE_EXTENSIONS + ": [" + ", ".join(str(x) for x in self.getFileExtensions()) + "]")
        print(OPTIONNAME_FEEDBACK_TEMPLATE + ": " + self.getFeedbackTemplate())
