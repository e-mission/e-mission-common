import emcommon.logger as Log
import emcommon.util as emcu
from .__testing import jest_test, _expect as expect, jest_describe


@jest_test
async def test_read_json_resource():
    result = await emcu.read_json_resource('label-options.default.json')
    # result['MODE'] should contain a mode with value 'taxi'
    expect(any([mode['value'] == 'taxi' for mode in result['MODE']]))


@jest_test
async def test_fetch_url():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    result = await emcu.fetch_url(url)
    expect(result['title'] ==
           'sunt aut facere repellat provident occaecati excepturi optio reprehenderit')


jest_describe('test_example')
