#!/bin/env python3
import multiprocessing
import datetime
import time
import numpy as np

def compute_heavy_task(task_queue):
    """A function that performs heavy compute and memory-intensive tasks."""
    while True:
        if not task_queue.empty():
            task_queue.get()
            large_array = np.random.rand(1000, 1000)
            np.linalg.inv(large_array)  # Inverting a large matrix
            task_queue.put(1)           # Indicate one task completed

def report_speed(task_queue, stop_event):
    """Report the speed of tasks completed per second."""
    total_tasks = 0
    while not stop_event.is_set():
        current_tasks = 0
        while not task_queue.empty():
            task_queue.get()
            current_tasks += 1
        total_tasks += current_tasks
        if current_tasks > 0:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} Cores: {num_processors} Tasks/second: {current_tasks}")
        time.sleep(1)
    print(f"Total tasks completed: {total_tasks}")

if __name__ == "__main__":
    num_processors = multiprocessing.cpu_count()

    task_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()

    # Start task processes
    processes = [multiprocessing.Process(target=compute_heavy_task, args=(task_queue,)) for _ in range(num_processors)]
    for p in processes:
        p.start()

    # Start reporting speed
    reporter = multiprocessing.Process(target=report_speed, args=(task_queue, stop_event))
    reporter.start()

    try:
        while True:
            task_queue.put(0)  # Add dummy task to keep the queue from being empty
            time.sleep(0.01)  # Adjust as needed for task frequency
    except KeyboardInterrupt:
        stop_event.set()
        for p in processes:
            p.terminate()
        reporter.terminate()
        print("\nInterrupted by user")

