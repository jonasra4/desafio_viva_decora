from queue import Queue
import threading, time, random

jobs = Queue()

def do_stuff(q):
    while not q.empty():
        value = q.get()
        time.sleep(random.randint(1, 10))
        print(value)
        q.task_done()

for i in range(10):
    jobs.put(i)

for i in range(3):
    worker = threading.Thread(target=do_stuff, args=(jobs,))
    worker.start()
    worker.join()
    print("all done")

print("waiting for queue to complete", jobs.qsize(), "tasks")
