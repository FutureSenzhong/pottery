# --------------------------------------------------------------------------- #
#   test_monkey.py                                                            #
#                                                                             #
#   Copyright © 2015-2021, Rajiv Bakulesh Shah, original author.              #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at:                                  #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# --------------------------------------------------------------------------- #


import json

from tests.base import TestCase  # type: ignore


class MonkeyPatchTests(TestCase):
    def test_json_encoder(self):
        try:
            json.dumps(object())
        except TypeError as error:
            assert str(error) in {
                "Object of type 'object' is not JSON serializable",  # Python 3.6
                'Object of type object is not JSON serializable',    # Python 3.7+
            }

    def test_redis_lolwut(self):
        lolwut = self.redis.lolwut().decode('utf-8')
        assert 'Redis ver.' in lolwut

        lolwut = self.redis.lolwut(5, 6, 7, 8).decode('utf-8')
        assert 'Redis ver.' in lolwut
