# prereq packages:
# python-git
# docker-engine

import git
import os
import re
import shutil
import subprocess
import tempfile
import unittest

class Assignment1(unittest.TestCase):
  def setUp(self):
    self.tmpdir = tempfile.mkdtemp()
    os.chdir(self.tmpdir)
    self.github_url = "https://github.com/jfarrell468/nginx-configparser"
    self.docker_image = re.sub('\W', '-', self.github_url)

  def tearDown(self):
    shutil.rmtree(self.tmpdir)

  def ValidateUrl(self):
    self.assertTrue('github.com' in self.github_url)

  def CloneRepository(self):
    git.Repo.clone_from(self.github_url, self.tmpdir)

  def MakefileExists(self):
    pass

  # TODO: Use https://github.com/docker/docker-py
  def BuildDockerImage(self):
    dockerfile = 'Dockerfile'
    self.assertFalse(os.path.isfile(dockerfile))
    with open(dockerfile, 'w') as f:
      f.write('''FROM ubuntu:14.04

RUN apt-get update && apt-get install --auto-remove -y make g++

WORKDIR /var/build
COPY . /var/build

RUN g++ -fprofile-arcs -ftest-coverage -std=c++0x -isystem gtest-1.7.0/include -Igtest-1.7.0 -pthread gtest-1.7.0/src/gtest-all.cc config_parser_test.cc config_parser.cc gtest-1.7.0/src/gtest_main.cc -o config_parser_test
''')
    subprocess.call(['docker', 'build', '-f', dockerfile, '-t', self.docker_image, self.tmpdir])

  def RunTestsInDocker(self):
    subprocess.call(['docker', 'run', ':'.join([self.docker_image, 'latest']), './config_parser_test'])

  def RunCoverageInDocker(self):
    subprocess.call(['docker', 'run', '--rm', ':'.join([self.docker_image, 'latest']), 'bash', '-c', './config_parser_test && gcov config_parser.cc'])

  def runTest(self):
    self.ValidateUrl()
    self.CloneRepository()
    self.BuildDockerImage()
    self.RunTestsInDocker()
    self.RunCoverageInDocker()


if __name__ == '__main__':
  unittest.main()
