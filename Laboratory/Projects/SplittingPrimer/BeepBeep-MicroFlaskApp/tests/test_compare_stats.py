from pyquery import PyQuery as pq
from tests.user_context import *


def test_compare_two_run(client, requests_mock):
    with UserContext(client, requests_mock) as uc:
        response = client.post('/comparisons', data={"runs":[1,2]})
        html = pq(response.data)

        # For titles
        run_title_list = []
        for i in html.items('.title'):
            run_title_list.append(i.text())
            
        assert run_title_list[0] == UserContext.mockruns[0]['title']
        assert run_title_list[1] == UserContext.mockruns[1]['title']

        # For average speeds
        run_speed_list = []
        for i in html.items('.average_speed'):
            run_speed_list.append(i.text())
            
        assert run_speed_list[0] == str(UserContext.mockruns[0]['average_speed'])
        assert run_speed_list[1] == str(UserContext.mockruns[1]['average_speed'])

        # For elapsed times
        run_time_list = []
        for i in html.items('.elapsed_time'):
            run_time_list.append(i.text())
            
        assert run_time_list[0] == str(UserContext.mockruns[0]['elapsed_time'])
        assert run_time_list[1] == str(UserContext.mockruns[1]['elapsed_time'])

