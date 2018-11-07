#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import hamcrest
from prego import Task, TestCase, running


class Test(TestCase):
    def test_factorial(self):
        Task().command('make clean all')

        server = Task('server', detach=True)
        server.command('./factorial_server', expected=-15)

        client = Task('client')
        client.assert_that(server, running())
        client.command('./factorial_client localhost 8')
        client.assert_that(client.lastcmd.stdout.content,
                           hamcrest.contains_string('factorial(8): 40320'))
