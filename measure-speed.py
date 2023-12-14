#!/bin/env python3
import multiprocessing
import datetime
import time
import numpy as np
import socket

def compute_heavy_task():
    """A function that performs highly CPU-intensive tasks."""
    while True:
        large_array = np.random.rand(2000, 2000)  # Increased matrix size
        np.linalg.inv(large_array)  # Inverting a large matrix
        np.dot(large_array, large_array.T)  # Matrix multiplication

def report_speed(task_counter, num_processors, stop_event):
    """Report the speed of tasks completed per second."""
    last_count = 0
    while not stop_event.is_set():
        current_count = task_counter.value
        tasks_completed = current_count - last_count
        last_count = current_count
        if tasks_completed > 0:
            hostname = socket.gethostname()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} {hostname} Cores: {num_processors} Tasks/second: {tasks_completed}")
        time.sleep(1)

if __name__ == "__main__":
    num_processors = multiprocessing.cpu_count()

    task_counter = multiprocessing.Value('i', 0)
    stop_event = multiprocessing.Event()

    # Start task processes
    processes = [multiprocessing.Process(target=compute_heavy_task) for _ in range(num_processors)]
    for p in processes:
        p.start()

    # Start reporting speed
    reporter = multiprocessing.Process(target=report_speed, args=(task_counter, num_processors, stop_event))
    reporter.start()

    try:
        while True:
            with task_counter.get_lock():
                task_counter.value += 1
            time.sleep(0.01)  # Adjust as needed for task frequency
    except KeyboardInterrupt:
        stop_event.set()
        for p in processes:
            p.terminate()
        reporter.terminate()
        print("\nInterrupted by user")
