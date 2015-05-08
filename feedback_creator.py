import os
import tutortool_plugin as ttp
import infocolor as ic


class FeedBackCreator(ttp.TutorToolPlugin):
    def __init__(self, config):
        ttp.TutorToolPlugin.__init__(self, config)

    def create_feedback_files(self, ex_list):
        if os.path.exists(self.feedback_template()):
            template = open(self.feedback_template(), 'r')
            template_content = template.read()
            template.close()
            print_template = True
        else:
            print_template = False
        for repo in self.repo_list():
            for ex in ex_list:
                current_template_content = template_content.replace("$NAME", repo).replace("$EX", ex)
                local_repo_ex_path = os.path.join(self.local_path(), repo, ex)
                if os.path.isdir(local_repo_ex_path):
                    feedback_name = "Feedback-" + repo + "-" + ex + ".txt"
                    feedback_path = os.path.join(local_repo_ex_path, feedback_name)
                    feedback_file = open(feedback_path, 'w')
                    if print_template:
                        feedback_file.write(current_template_content)
                    feedback_file.close()
                    ic.Info.printm("Created in " + repo + ": " + feedback_path)
                else:
                    ic.Info.printe(ex + " not present in " + repo)