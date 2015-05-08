import os
import pysvn
import tutortool_plugin as ttp
import datetime
import time
import shutil
import infocolor as ic


class MultiSVN(ttp.TutorToolPlugin):
    def __init__(self, config, username, password):
        ttp.TutorToolPlugin.__init__(self, config)
        self.client = pysvn.Client()
        self.client.callback_get_login = self.svn_credentials(username, password)
        self.client.callback_ssl_server_trust_prompt = self.ssl_server_trust_prompt

    def svn_credentials(self, user, password):
        def get_login(realm, username, may_save):
            return True, user, password, False
        return get_login

    def ssl_server_trust_prompt(self, trust_dict):
    	return True, trust_dict['failures'], False

    def add(self):
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            status_list = self.client.status(local_repo_path)
            for file_name in status_list:
                if "Feedback-" in file_name.path and not file_name.is_versioned:
                    ic.Info.printm("Added to " + repo + ": " + file_name.path)
                    self.client.add(file_name.path)

    def checkout(self, last_monday=False):
        last_monday_date, last_monday_in_seconds = self.last_monday_timestamp()
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            svn_repo_address = os.path.join(self.svn_root_address(), repo)
            if last_monday:
                self.client.checkout(svn_repo_address, local_repo_path, revision=pysvn.Revision(pysvn.opt_revision_kind.date, last_monday_in_seconds))
                ic.Info.printi("Check out " + repo + " on last Monday " + last_monday_date.__str__())
            else:
                self.client.checkout(svn_repo_address, local_repo_path)
                ic.Info.printi("Check out " + repo)

    def update(self, last_monday=False):
        last_monday_date, last_monday_in_seconds = self.last_monday_timestamp()
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            if last_monday:
                self.client.update(local_repo_path, revision=pysvn.Revision(pysvn.opt_revision_kind.date, last_monday_in_seconds))
                ic.Info.printi("Update " + repo + " to last Monday " + last_monday_date.__str__())
            else:
                self.client.update(local_repo_path)
                ic.Info.printi("Update " + repo)

    def last_monday_timestamp(self):
        today = datetime.date.today()
        offset = today.weekday() % 7
        last_monday_day = today - datetime.timedelta(days=offset)
        last_monday_combined = datetime.datetime.combine(last_monday_day, datetime.time(0, 1))
        time_stamp = time.mktime(last_monday_combined.timetuple())
        return last_monday_combined, time_stamp

    def commit(self, commit_message):
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            self.client.checkin(local_repo_path, commit_message)
            ic.Info.printi("Commit " + repo + " with message: \"commit_message\"")

    def addci(self, commit_message):
        self.add()
        self.commit(commit_message)

    def revert(self):
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            self.client.revert(local_repo_path)
            ic.Info.printi("Revert " + repo)

    def clean(self):
        for repo in self.repo_list():
            local_repo_path = os.path.join(self.local_path(), repo)
            shutil.rmtree(local_repo_path)
            ic.Info.printi("Remove " + repo)
