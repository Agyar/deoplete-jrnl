"""
jrnl completer
"""
# Copyright (c) 2018 Benjamin Lorendeau. All rights reserved.
# Use of this source code is governed by an MIT license that can be
# found in the LICENSE file.

import re
import subprocess

from .base import Base  # pylint: disable=E0401

# pylint: disable=W0201,W0613
class Source(Base):
    """
    General completer that provides Jrnl tag names in completions
    """

    TAG_PATTERN = re.compile(r'@\w?')

    def __init__(self, vim):
        super().__init__(vim)

        self.__cache = []

        self.filetypes = ['text']
        self.mark = '[jrnl]'
        self.min_pattern_length = 0
        self.name = 'jrnl'
        self.input_patterns = {'@'}
        self.kind = 'keyword'

    def on_init(self, context):
        """ build cache of jrnl tags """
        jrnl_out = subprocess.check_output('jrnl --tags', shell=True)
        candidates = re.findall(r'@\w+', jrnl_out.decode('utf-8'))
        self.__cache = [{'word': candidate[1:]} for candidate in candidates]

    def get_complete_position(self, context):
        """ define position to where should this be activated """
        pat = None
        pattern = self.TAG_PATTERN.finditer(context['input'])
        for pruning in pattern:
            pat = pruning
        return pat.end() if pat is not None else -1

    def gather_candidates(self, context):
        """ enable output on tagging """
        if self.TAG_PATTERN.search(context['input']) is not None:
            return self.__cache
        return None
