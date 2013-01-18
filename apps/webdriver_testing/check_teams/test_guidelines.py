# -*- coding: utf-8 -*-
from apps.webdriver_testing.webdriver_base import WebdriverTestCase
from apps.webdriver_testing.pages.site_pages.teams import messages_tab
from apps.webdriver_testing.pages.site_pages.teams import tasks_tab
from apps.webdriver_testing.data_factories import TeamMemberFactory
from apps.webdriver_testing.data_factories import TeamLangPrefFactory
from apps.webdriver_testing.data_factories import TeamContributorMemberFactory
from apps.webdriver_testing.data_factories import WorkflowFactory
from apps.webdriver_testing.data_factories import UserFactory
from apps.webdriver_testing import data_helpers
import time

class TestCaseTeamGuidelines(WebdriverTestCase):    

    _TEST_GUIDELINES = {
        'SUBTITLE': ('The are the guidelines for subtitling for this team.'),
        'TRANSLATE': ('Do not just use google translate!'),
        'REVIEW': ('The Review process is very important. Check everything.')
        }

    def setUp(self):
        WebdriverTestCase.setUp(self)
        self.data_utils = data_helpers.DataHelpers()
        self.messages_tab = messages_tab.MessagesTab(self)
        self.tasks_tab = tasks_tab.TasksTab(self)
        self.team_owner = UserFactory.create()

        #CREATE AN OPEN TEAM WITH WORKFLOWS and AUTOTASKS
        self.team = TeamMemberFactory.create(team__workflow_enabled = True,
                                             user = self.team_owner).team
        #Turn on Task Autocreation
        WorkflowFactory.create(
            team = self.team,
            autocreate_subtitle = True,
            autocreate_translate = True,
            review_allowed = 10)


        #ADD THE TEST MESSAGES TO THE TEST TEAM
        self.messages_tab.open_messages_tab(self.team.slug)

        self.messages_tab.log_in(self.team_owner.username, 'password')
        self.messages_tab.open_messages_tab(self.team.slug)
        self.messages_tab.edit_guidelines(self._TEST_GUIDELINES)
 


    def test_guidelines__edit(self):
        """Change the default guidelines and verify they are stored.

        """
        self.assertEqual(self._TEST_GUIDELINES, 
            self.messages_tab.stored_guidelines())

