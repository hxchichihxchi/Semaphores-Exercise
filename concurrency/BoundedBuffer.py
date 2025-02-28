"""
Enhanced Bounded Buffer Implementation with Detailed Documentation

This module implements the classic producer-consumer problem solution using semaphores,
demonstrating thread synchronization concepts with detailed logging for educational purposes.
"""

from semaphore import semaphore  # Custom semaphore implementation
import time                     # For timestamp generation
import threading                # For thread management and locks

class BoundedBuffer:
    def __init__(self, size) -> None:
        """
        Initializes buffer with synchronization primitives and state tracking.
        
        Args:
            size: Maximum capacity of the buffer (integer)
        """
        # Set buffer capacity from parameter
        self.buffer_size = size
        
        # Initialization log message with current time
        print(f"[{time.strftime('%H:%M:%S')}] Creating Bounded Buffer with size {size}")
        
        # Semaphore tracking available empty slots (initialized to full capacity)
        # Named for clearer debug output
        self.semaphore_empty = semaphore(size, "Empty_Slots")
        
        # Semaphore tracking filled slots (initialized to 0)
        self.semaphore_full = semaphore(0, "Full_Slots")
        
        # Shared buffer storage (list acting as queue)
        self.buffer = []
        
        # Mutex lock to protect buffer access (ensures atomic operations)
        self.buffer_lock = threading.Lock()
        
        # Initial state log
        print(f"[{time.strftime('%H:%M:%S')}] Bounded Buffer initialized: Empty={size}, Full=0")

    def produce(self, item):
        """
        Producer method: Adds items to buffer with full synchronization.
        
        Args:
            item: Data item to be added to the buffer
        """
        # Get current thread identifier for logging
        thread_id = threading.current_thread().name
        
        # Display pre-production state (within lock for accurate snapshot)
        with self.buffer_lock:  # Acquire mutex
            # Log production attempt with current buffer state
            print(f"\n[{time.strftime('%H:%M:%S')}] Producer {thread_id} attempting to produce item {item}")
            print(f"[{time.strftime('%H:%M:%S')}] Current buffer: {self.buffer} [{len(self.buffer)}/{self.buffer_size}]")
        
        # Block if no empty slots (wait operation on empty semaphore)
        if self.semaphore_empty.value <= 0:
            print(f"[{time.strftime('%H:%M:%S')}] Buffer FULL! Producer {thread_id} must wait...")
        
        
        
        # Critical Section: Actual item production
        with self.buffer_lock:  # Acquire mutex
            self.semaphore_empty.P()  # Decrement empty count (may block)
            self.buffer.append(item)  # Add item to end of buffer
            # Log successful production
            print(f"[{time.strftime('%H:%M:%S')}] Producer {thread_id} PRODUCED item {item}")
            print(f"[{time.strftime('%H:%M:%S')}] Buffer after production: {self.buffer} [{len(self.buffer)}/{self.buffer_size}]")
        
        # Signal availability of new item (increment full count)
        self.semaphore_full.V()

    def consume(self):
        """
        Consumer method: Removes and returns items from buffer with synchronization.
        
        Returns:
            The consumed item from buffer front (FIFO order)
        """
        # Get current thread identifier
        thread_id = threading.current_thread().name
        
        # Display pre-consumption state
        with self.buffer_lock:  # Acquire mutex
            # Log consumption attempt
            print(f"\n[{time.strftime('%H:%M:%S')}] Consumer {thread_id} attempting to consume an item")
            print(f"[{time.strftime('%H:%M:%S')}] Current buffer: {self.buffer} [{len(self.buffer)}/{self.buffer_size}]")
        
        # Block if no available items (wait operation on full semaphore)
        if self.semaphore_full.value <= 0:
            print(f"[{time.strftime('%H:%M:%S')}] Buffer EMPTY! Consumer {thread_id} must wait...")
        
        # Critical Section: Actual item consumption
        with self.buffer_lock:  # Acquire mutex

            self.semaphore_full.P()  # Decrement full count (may block)
            item = self.buffer.pop(0)  # Remove first item (FIFO)

            # Log successful consumption
            print(f"[{time.strftime('%H:%M:%S')}] Consumer {thread_id} CONSUMED item {item}")
            print(f"[{time.strftime('%H:%M:%S')}] Buffer after consumption: {self.buffer} [{len(self.buffer)}/{self.buffer_size}]")
        
        # Signal new empty slot availability
        self.semaphore_empty.V()  # Increment empty count
        
        return item  # Return consumed item to caller