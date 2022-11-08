#!/usr/bin/python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from plugins import issue
from plugins import repository


class MyTool():

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description='MyTool doing nice things'
        )
        parser.add_argument(
            '--config',
            default='config.yaml',
            help='My config file'
        )
        self.createCommandParsers(parser)
        return parser

    def createCommandParsers(self, parser):
        subparsers = parser.add_subparsers(title='commands')

        self.add_repository_subparser(subparsers)
        self.add_issue_subparser(subparsers)

        return subparsers

    def add_repository_subparser(self, subparsers):
        cmd_repository = subparsers.add_parser(
            'repository',
            help='Repository parser')
        cmd_rep_subparsers = cmd_repository.add_subparsers()

        self.add_rep_create_subparser(cmd_rep_subparsers)
        self.add_rep_close_subparser(cmd_rep_subparsers)

    def add_rep_close_subparser(self, subparsers):
        cmd_rep_close = subparsers.add_parser(
            'close',
            help='Rep closer'
        )
        cmd_rep_close.add_argument(
            '--pr',
            action='store_true',
            help='Close Pull Requests'
        )

        cmd_rep_close.set_defaults(func=self.rep_close_pr)

    def add_rep_create_subparser(self, subparsers):
        cmd_rep_create = subparsers.add_parser(
            'create',
            help='Rep create'
        )
        cmd_rep_create.add_argument(
            '--pr',
            action='store_true',
            help='Create Pull Requests'
        )

        cmd_rep_create.set_defaults(func=self.rep_create_pr)

    def add_issue_subparser(self, subparsers):
        cmd_issue = subparsers.add_parser(
            'issue',
            help='issue parser')
        cmd_issue_subparsers = cmd_issue.add_subparsers()

        self.add_issue_list_subparser(cmd_issue_subparsers)

    def add_issue_list_subparser(self, subparsers):
        cmd_issue_list = subparsers.add_parser(
            'list',
            help='Issue lister'
        )
        cmd_issue_list.add_argument(
            '--open',
            action='store_true',
            help='List open issues'
        )
        cmd_issue_list.add_argument(
            '--closed',
            action='store_true',
            help='List closed issues'
        )

        cmd_issue_list.set_defaults(func=self.issue_lister)

    def issue_lister(self):
        if self.args.open:
            issue.Issue.list_open()
        elif self.args.closed:
            issue.Issue.list_closed()

    def rep_close_pr(self):
        if self.args.pr:
            repository.Repository.close_pr()

    def rep_create_pr(self):
        if self.args.pr:
            repository.Repository.create_pr()

    def parse_arguments(self, args=None):
        self.parser = self.create_parser()
        self.args = self.parser.parse_args(args)

    def main(self, args=None):
        self.parse_arguments(args)
        print(self.args)

        self.args.func()


def main():
    MyTool().main()


if __name__ == '__main__':
    main()
