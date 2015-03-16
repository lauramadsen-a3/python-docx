# encoding: utf-8

"""
Test suite for the docx.parts.settings module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.settings import SettingsPart
from docx.settings import Settings

from ..unitutil.cxml import element
from ..unitutil.mock import class_mock, instance_mock, method_mock


class DescribeSettingsPart(object):

    def it_is_used_by_loader_to_construct_settings_part(self, load_fixture):
        partname, content_type, blob, package_, settings_part_ = load_fixture
        part = PartFactory(partname, content_type, None, blob, package_)
        SettingsPart.load.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is settings_part_

    def it_provides_access_to_its_settings(self, settings_fixture):
        settings_part, Settings_, settings_ = settings_fixture
        settings = settings_part.settings
        Settings_.assert_called_once_with(settings_part.element)
        assert settings is settings_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def load_fixture(self, load_, package_, settings_part_):
        partname, blob = 'partname', 'blob'
        content_type = CT.WML_SETTINGS
        load_.return_value = settings_part_
        return partname, content_type, blob, package_, settings_part_

    @pytest.fixture
    def settings_fixture(self, Settings_, settings_):
        settings_elm = element('w:settings')
        settings_part = SettingsPart(None, None, settings_elm, None)
        return settings_part, Settings_, settings_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def load_(self, request):
        return method_mock(request, SettingsPart, 'load')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def Settings_(self, request, settings_):
        return class_mock(
            request, 'docx.parts.settings.Settings', return_value=settings_
        )

    @pytest.fixture
    def settings_(self, request):
        return instance_mock(request, Settings)

    @pytest.fixture
    def settings_part_(self, request):
        return instance_mock(request, SettingsPart)