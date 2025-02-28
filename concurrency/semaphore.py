import threading       #
import time


class semaphore:
    def __init__(self, initial_value, name='semaphore'): #Constructor
        # Conditinoal variable to lock and notify processes
        self.lock = threading.Condition(threading.Lock())

        # current semaphore value
        self.value = initial_value

        self.name = name

        # log to show starting time
        print(f"[{time.strftime('%H:%M:%S')}] {self.name} initialized with value {self.value}")

    def P(self):
        """
        Decrease semeaphre value
        Implement wait operation with blocking when resources are unavaible
        """
        # get the current thread name for logging
        thread_id = threading.current_thread().name

        # Enter the condition variable to acquire the lock
        with self.lock:
            # Check if resources are available
            if self.value <= 0:
                print(f"[{time.strftime('%H:%M:%S')}] {self.name} value is {self.value}, Thread {thread_id} BLOCKED")

            #  Handle spurios wakeups
            while self.value <= 0:
                self.lock.wait()
                print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} WOKE UP, value is now {self.value}")
            
            # Decrease semaphore value (acquire the resource)
            self.value = self.value - 1
            print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} acquired {self.name}, value is decreased to {self.value}")

    def V(self):
        """
        Increase the semaphore value (release resource)
        Implement the signal operation to notify waiting threads
        """

        # get the current thread
        thread_id = threading.current_thread().name

        # Show the release attempt
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} releasing {self.name}")

        # Enter condition varaible block
        with self.lock:
            # Increasing the resource count (release a resoource)
            self.value += 1
            print(f"[{time.strftime('%H:%M:%S')}] {self.name} value increased to {self.value}")

            # wake up waiting threads (if any)
            self.lock.notify()

            print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} notified waiting threads")


