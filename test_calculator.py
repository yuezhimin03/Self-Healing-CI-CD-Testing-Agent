from calculator import add, multiply

def test_add():
    assert add(2, 3) == 5

def test_multiply():
    # 这里期望 2 * 3 = 6，但由于源码的 Bug，它会返回 5，触发测试失败
    assert multiply(2, 3) == 6