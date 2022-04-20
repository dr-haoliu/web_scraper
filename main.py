# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import multiprocessing
from multiprocessing import Process, Manager, Semaphore
import pprint

def sum_all(value):

    return sum(range(1, value + 1))

def dict_all(d, value, sema):
    d[value] = "Hi, I was written by process %d" % value
    sema.release()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    pool_obj = multiprocessing.Pool()
    answer = pool_obj.map(sum_all, range(0, 5))
    print(answer)

    numberOfThreads = 2
    concurrency = 2
    total_task_num = 50
    sema = Semaphore(concurrency)
    with Manager() as manager:
        d = manager.dict()
        # jobs = [Process(target=dict_all, args=(d, i)) for i in range(5)]
        all_processes = []
        for i in range(total_task_num):
            # once 20 processes are running, the following `acquire` call
            # will block the main process since `sema` has been reduced
            # to 0. This loop will continue only after one or more
            # previously created processes complete.
            sema.acquire()
            p = Process(target=dict_all, args=(d, i, sema))
            all_processes.append(p)
            p.start()
        # `d` is a DictProxy object that can be converted to dict
        # _ = [p.start() for p in jobs]
        # _ = [p.join() for p in jobs]
        # inside main process, wait for all processes to finish
        for p in all_processes:
            p.join()

        pprint.pprint(dict(d))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
