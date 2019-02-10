def assert_error(response_msg, expected_msg):
    assert response_msg.decode('UTF-8') == expected_msg
