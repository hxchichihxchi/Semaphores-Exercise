import time
import threading
import random
from semaphore import semaphore

class criticalSection:
    def __init__(self):
        # Create a binary semaphore (mutex) with initial value 1
        # Name it to help with logging
        self.semaphore = semaphore(1, "CS_mutex")

        # Log the initialization
        print(f"[{time.strftime('%H:%M:%S')}] critical section initialized")
    
    def critical_section(self, p):
        """
        1. Entry section: request access to CS
        2. Critical section: executed protected code/access shared resource
        3. Exit section: Release access to the shared resource
        """

        # get the current current thread
        thread_id = threading.current_thread().name

        # -- ENTRY SECTION --
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} ATTEMPTING CS")
        self.semaphore.P() # Semaphore acquire operation (decrease value)

        # -- CRITICAL SECTION -- 
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} ENTERED CS")
        # simulate cs
        cpu_time = random.uniform(1, 3)
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} RUNNING CS for {cpu_time}")
        time.sleep(cpu_time)

        # -- EXIT SECTION --
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} EXITING CS")
        self.semaphore.V() # release the resource (increase value)

        # -- REMAINDER SECTIONO --
        print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} LEFT the CS")

