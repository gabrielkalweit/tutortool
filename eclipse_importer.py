import os
import shutil
import tutortool_plugin as ttp
import infocolor as ic


class EclipseImporter(ttp.TutorToolPlugin):
    def __init__(self, config):
        ttp.TutorToolPlugin.__init__(self, config)

    def import_projects(self, ex_list):
        if os.path.isdir(self.local_eclipse_path()):
            self.delete_local_eclipse_path()
        os.makedirs(self.local_eclipse_path())
        for repo in self.repo_list():
            reduced_ex_list = self.check_ex(ex_list, repo)
            if not reduced_ex_list:
                ic.Info.printe("No ex in " + repo)
                continue
            os.makedirs(os.path.join(self.local_eclipse_path(), repo))
            self.create_project_file(repo, reduced_ex_list)
            self.create_classpath_file(repo, reduced_ex_list)
            ic.Info.printi("Import " + repo)

    def check_ex(self, ex_list, repo):
        reduced_ex_list = []
        for ex in ex_list:
            local_ex_path = os.path.join(self.local_path(), repo, ex)
            if not os.path.isdir(local_ex_path):
                ic.Info.printw(ex + " not present in " + repo)
            else:
                reduced_ex_list.append(ex)
        return reduced_ex_list

    def delete_local_eclipse_path(self):
        shutil.rmtree(self.local_eclipse_path())

    def create_project_file(self, repo, ex_list):
        project = open(os.path.join(self.local_eclipse_path(), repo, ".project"), 'w')
        project.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        project.write("<projectDescription>\n")
        project.write("\t<name>" + repo + "</name>\n")
        project.write("\t<comment></comment>\n")
        project.write("\t<projects>\n")
        project.write("\t</projects>\n")
        project.write("\t<buildSpec>\n")
        project.write("\t\t<buildCommand>\n")
        project.write("\t\t\t<name>org.eclipse.jdt.core.javabuilder</name>\n")
        project.write("\t\t\t<arguments>\n")
        project.write("\t\t\t</arguments>\n")
        project.write("\t\t</buildCommand>\n")
        project.write("\t</buildSpec>\n")
        project.write("\t<natures>\n")
        project.write("\t\t<nature>org.eclipse.jdt.core.javanature</nature>\n")
        project.write("\t</natures>\n")
        project.write("\t<linkedResources>\n")
        for ex in ex_list:
            local_ex_path = os.path.join(self.local_path(), repo, ex)
            if os.path.isdir(os.path.join(local_ex_path, "src")):
                project.write("\t\t<link>\n")
                project.write("\t\t\t<name>" + ex + "</name>\n")
                project.write("\t\t\t<type>2</type>\n")
                project.write("\t\t\t<location>" + os.path.join(local_ex_path, "src").replace("\\", "/") + "</location>\n")
                project.write("\t\t</link>\n")
            file_list = [ f for f in os.listdir(local_ex_path) for extension in self.file_extensions() if f.endswith(extension) ]
            for f in file_list:
                file_path = os.path.join(local_ex_path, f)
                project.write("\t\t<link>\n")
                name = f if f.startswith("Feedback") else ex + "-" + f
                project.write("\t\t\t<name>" + name + "</name>\n")
                project.write("\t\t\t<type>1</type>\n")
                project.write("\t\t\t<location>" + file_path.replace("\\", "/") + "</location>\n")
                project.write("\t\t</link>\n")
        project.write("\t</linkedResources>\n")
        project.write("</projectDescription>\n")
        project.close()

    def create_classpath_file(self, repo, ex_list):
        classpath = open(os.path.join(self.local_eclipse_path(), repo, ".classpath"), 'w')
        classpath.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<classpath>\n")
        for ex in ex_list:
            if os.path.isdir(os.path.join(self.local_path(), repo, ex, "src")):
                classpath.write("\t<classpathentry kind=\"src\" path=\"" + ex + "\"/>\n")
        classpath.write("\t<classpathentry kind=\"con\" path=\"org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8\"/>\n")
        classpath.write("\t<classpathentry kind=\"con\" path=\"org.eclipse.jdt.junit.JUNIT_CONTAINER/4\"/>\n")
        classpath.write("\t<classpathentry kind=\"output\" path=\"bin\"/>\n")
        classpath.write("</classpath>\n")
        classpath.close()