import os
import logging
import yaml
import shutil
import pkg_resources

class Project:

    __descriptor_name__ = 'project.yaml'

    def __init__(self, prj_root, workspace):
        self.prj_root = prj_root
        self.log = logging.getLogger(__name__)

    def create_prj(self):
        self._create_dirs()
        self._create_prj_stub()

    def _create_dirs(self):
        """
        Creates the directory tree of the project
        :return:
        """

        directories = {'sources', 'dependencies', 'deployment'}
        src_subdirs = {'ssm', 'pattern', 'vnf'}

        os.makedirs(self.prj_root, exist_ok=False)
        for d in directories:
            path = os.path.join(self.prj_root, d)
            os.makedirs(path, exist_ok=True)

        src_path = os.path.join(self.prj_root, 'sources')
        for d in src_subdirs:
            path = os.path.join(src_path, d, 'sample')
            os.makedirs(path, exist_ok=True)
            self._create_sample(d, path)
        self._create_vnf_dir()

    def _create_vnf_dir(self, name='sample'):
        """
        Function to create a new VNF inside project source.
        :param name:The VNF name
        """
        vnf_subdirs = {'fsm'}
        vnf_path = os.path.join(self.prj_root, 'sources', 'vnf', name)
        self._create_sample('vnf', vnf_path)
        for d in vnf_subdirs:
            path = os.path.join(vnf_path, d)
            os.makedirs(path, exist_ok=False)

    def _create_prj_stub(self):
        """
        Creates the project descriptor (project.yaml)
        :return:
        """
        d = {
            'name': 'sonata-project-sample',
            'group': 'eu.sonata.project',
            'version': '0.0.1',
            'maintainer': 'Name, Company, Contact',
            'description': 'Project description',
            'catalogues': ['personal'],
            'publish_to': ['personal']
        }

        prj_path = os.path.join(self.prj_root, Project.__descriptor_name__)
        with open(prj_path, 'w') as prj_file:
            prj_file.write(yaml.dump(d))

    def _create_sample(self, prj_type, path):
        switcher = {
            # 'fsm': self._create_sample_fsm,
            'ssm': self._create_sample_ssm,
            'pattern': self._create_sample_pattern,
            'vnf': self._create_sample_vnf
        }
        func = switcher.get(prj_type)
        if func is None:
            self.log.error("Could not create sample for " + prj_type + ", unknown project type")
            return
        func(path)

    def _create_sample_fsm(self, path):
        d = {
            'name': 'sample fsm',
            'id': 'com.sonata.fsm.sample',
            'version': '0.1'
        }
        prj_path = os.path.join(path, 'fsm.yaml')
        with open(prj_path, 'w') as prj_file:
            prj_file.write(yaml.dump(d))

    def _create_sample_ssm(self, path):
        d = {
            'name': 'sample ssm',
            'id': 'com.sonata.ssm.sample',
            'version': '0.1'
        }
        prj_path = os.path.join(path, 'ssm.yaml')
        with open(prj_path, 'w') as prj_file:
            prj_file.write(yaml.dump(d))

    def _create_sample_pattern(self, path):
        d = {
            'name': 'sample pattern',
            'id': 'com.sonata.pattern.sample',
            'version': '0.1'
        }
        prj_path = os.path.join(path, 'patterm.yaml')
        with open(prj_path, 'w') as prj_file:
            prj_file.write(yaml.dump(d))

    def _create_sample_vnf(self, path):
        """
        Create a sample VNF descriptor (to be evoked upon project creation)
        :param path: The VNF sample directory
        :return:
        """
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        dst = path
        shutil.copyfile(os.path.join(src, 'vnfd-sample.yaml'), os.path.join(dst, 'vnfd-sample.yaml'))
        shutil.copyfile(os.path.join(src, 'sample_docker'), os.path.join(dst, 'sample_docker'))
        shutil.copyfile(os.path.join(src, 'sample_docker'), os.path.join(dst, 'sample_docker'))