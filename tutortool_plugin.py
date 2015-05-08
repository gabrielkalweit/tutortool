class TutorToolPlugin:
    def __init__(self, config):
        self.config = config

    def repo_list(self):
        return self.config.getSvnRepositories()

    def svn_root_address(self):
        return self.config.getSvnRoot()

    def local_path(self):
        return self.config.getLocalTargetDir()

    def local_eclipse_path(self):
        return self.config.getLocalEclipseTargetDir()

    def feedback_template(self):
        return self.config.getFeedbackTemplate()

    def file_extensions(self):
        return self.config.getFileExtensions()