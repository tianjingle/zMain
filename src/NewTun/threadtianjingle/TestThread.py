import threadpool

class TestThread:
    def hello(self,m, n, o):
        for item in range(10000):
            print(item)
        print("m = %s, n = %s, o = %s" % (m, n, o))


if __name__ == '__main__':
    # 方法2
    dict_vars_1 = {'m': '1', 'n': '2', 'o': '3'}
    dict_vars_2 = {'m': '4', 'n': '5', 'o': '6'}
    func_var = [(None, dict_vars_1), (None, dict_vars_2)]
    pool = threadpool.ThreadPool(2)
    test=TestThread()
    requests = threadpool.makeRequests(test.hello, func_var)
    for req in requests:
        pool.putRequest(req)
    pool.wait()
    print("tianjingle")