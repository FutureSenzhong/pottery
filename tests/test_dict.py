# --------------------------------------------------------------------------- #
#   test_dict.py                                                              #
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


import collections
import json

from pottery import KeyExistsError
from pottery import RedisDict
from tests.base import TestCase  # type: ignore


class DictTests(TestCase):
    '''These tests come from these examples:
        https://docs.python.org/3/tutorial/datastructures.html#dictionaries
    '''

    def test_keyexistserror_raised(self):
        d = RedisDict(
            redis=self.redis,
            key='pottery:tel',
            sape=4139,
            guido=4127,
            jack=4098,
        )
        d   # Workaround for Pyflakes.  :-(
        with self.assertRaises(KeyExistsError):
            RedisDict(
                redis=self.redis,
                key='pottery:tel',
                sape=4139,
                guido=4127,
                jack=4098,
            )

    def test_keyexistserror_repr(self):
        d = RedisDict(
            redis=self.redis,
            key='pottery:tel',
            sape=4139,
            guido=4127,
            jack=4098,
        )
        d   # Workaround for Pyflakes.  :-(
        try:
            RedisDict(
                redis=self.redis,
                key='pottery:tel',
                sape=4139,
                guido=4127,
                jack=4098,
            )
        except KeyExistsError as wtf:
            assert repr(wtf) == (
                f"KeyExistsError(redis=Redis<ConnectionPool<Connection<host=localhost,port=6379,db={self.redis_db}>>>, "
                "key='pottery:tel')"
            )
        else:  # pragma: no cover
            self.fail(msg='KeyExistsError not raised')

    def test_keyexistserror_str(self):
        d = RedisDict(
            redis=self.redis,
            key='pottery:tel',
            sape=4139,
            guido=4127,
            jack=4098,
        )
        d   # Workaround for Pyflakes.  :-(
        try:
            RedisDict(
                redis=self.redis,
                key='pottery:tel',
                sape=4139,
                guido=4127,
                jack=4098,
            )
        except KeyExistsError as wtf:
            assert str(wtf) == (
                f"redis=Redis<ConnectionPool<Connection<host=localhost,port=6379,db={self.redis_db}>>> "
                "key='pottery:tel'"
            )
        else:  # pragma: no cover
            self.fail(msg='KeyExistsError not raised')

    def test_basic_usage(self):
        tel = RedisDict(redis=self.redis, jack=4098, sape=4139)
        tel['guido'] = 4127
        assert tel == {'sape': 4139, 'guido': 4127, 'jack': 4098}
        assert tel['jack'] == 4098
        del tel['sape']
        tel['irv'] = 4127
        assert tel == {'guido': 4127, 'irv': 4127, 'jack': 4098}
        assert sorted(tel) == ['guido', 'irv', 'jack']
        assert 'guido' in tel
        assert not 'jack' not in tel

    def test_init_with_key_value_pairs(self):
        d = RedisDict(
            [('sape', 4139), ('guido', 4127), ('jack', 4098)],
            redis=self.redis,
        )
        assert d == {'sape': 4139, 'jack': 4098, 'guido': 4127}

    def test_init_with_kwargs(self):
        d = RedisDict(redis=self.redis, sape=4139, guido=4127, jack=4098)
        assert d == {'sape': 4139, 'jack': 4098, 'guido': 4127}

    # The following tests come from these examples:
    #   https://docs.python.org/3.4/library/stdtypes.html#mapping-types-dict

    def test_more_construction_options(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        b = {'one': 1, 'two': 2, 'three': 3}
        c = RedisDict(zip(['one', 'two', 'three'], [1, 2, 3]), redis=self.redis)
        d = RedisDict([('two', 2), ('one', 1), ('three', 3)], redis=self.redis)
        e = RedisDict({'three': 3, 'one': 1, 'two': 2}, redis=self.redis)
        assert a == b == c == d == e

    def test_len(self):
        a = RedisDict(redis=self.redis)
        assert len(a) == 0
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert len(a) == 3
        a['four'] = 4
        assert len(a) == 4
        del a['four']
        assert len(a) == 3

    def test_repr(self):
        a = RedisDict(redis=self.redis, one=1, two=2)
        assert repr(a) in {
            "RedisDict{'one': 1, 'two': 2}",
            "RedisDict{'two': 2, 'one': 1}",
        }

    def test_update(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        a.update()
        assert a == {'one': 1, 'two': 2, 'three': 3}

        a.update({'four': 4, 'five': 5})
        assert a == {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}

        a.update((('six', 6), ('seven', 7)))
        assert a == {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
        }

        a.update(eight=8, nine=9)
        assert a == {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
        }

    def test_keyerror(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert a['one'] == 1
        assert a['two'] == 2
        assert a['three'] == 3
        with self.assertRaises(KeyError):
            a['four']

    def test_key_assignment(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=2)
        assert a['three'] == 2
        a['three'] = 3
        assert a['three'] == 3
        a['four'] = 4
        assert a['four'] == 4

    def test_key_deletion(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert sorted(a) == ['one', 'three', 'two']
        a['four'] = 4
        assert sorted(a) == ['four', 'one', 'three', 'two']
        with self.assertRaises(KeyError):
            del a['five']
        del a['four']
        assert sorted(a) == ['one', 'three', 'two']
        del a['three']
        assert sorted(a) == ['one', 'two']
        del a['two']
        assert sorted(a) == ['one']
        del a['one']
        assert sorted(a) == []
        with self.assertRaises(KeyError):
            del a['one']

    def test_key_membership(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert 'one' in a
        assert 'four' not in a
        assert not 'four' in a
        a['four'] = 4
        assert 'four' in a
        del a['four']
        assert 'four' not in a
        assert not 'four' in a

    def test_clear(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert sorted(a) == ['one', 'three', 'two']
        assert a.clear() is None
        assert sorted(a) == []
        assert a.clear() is None
        assert sorted(a) == []

    def test_get(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert a.get('one') == 1
        assert a.get('one', 42) == 1
        assert a.get('two') == 2
        assert a.get('two', 42) == 2
        assert a.get('three') == 3
        assert a.get('three', 42) == 3
        assert a.get('four') is None
        assert a.get('four', 42) == 42
        a['four'] = 4
        assert a.get('four') == 4
        assert a.get('four', 42) == 4
        del a['four']
        assert a.get('four') is None
        assert a.get('four', 42) == 42

    def test_items(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert isinstance(a.items(), collections.abc.ItemsView)
        assert len(a) == 3
        assert set(a.items()) == {('one', 1), ('two', 2), ('three', 3)}
        assert ('one', 1) in a.items()
        assert ('four', 4) not in a.items()

    def test_keys(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert isinstance(a.keys(), collections.abc.KeysView)
        assert len(a) == 3
        assert set(a.keys()) == {'one', 'two', 'three'}
        assert 'one' in a.keys()
        assert 'four' not in a.keys()

    def test_values(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert isinstance(a.values(), collections.abc.ValuesView)
        assert len(a) == 3
        assert set(a.values()) == {1, 2, 3}
        assert 1 in a.values()
        assert 4 not in a.values()

    def test_membership_for_non_jsonifyable_element(self):
        redis_dict = RedisDict(redis=self.redis)
        assert not BaseException in redis_dict

    def test_json_dumps(self):
        a = RedisDict(redis=self.redis, one=1, two=2, three=3)
        assert json.dumps(a) == '{"one": 1, "two": 2, "three": 3}'
