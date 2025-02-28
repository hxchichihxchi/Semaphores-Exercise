"""
Synchronization Demonstrations with Detailed Comments

This module showcases two fundamental concurrency problems:
1. Critical Section problem using mutual exclusion
2. Producer-Consumer problem using bounded buffers
with detailed logging to visualize thread interactions.
"""

# Import required modules
import threading  # For thread creation and management
import time       # For delays and timestamp generation
import random     # For simulating real-world processing variance
from criticalsection import criticalSection  # Mutual exclusion implementation
from BoundedBuffer import BoundedBuffer      # Producer-consumer implementation

def test_critical_section():
    """
    Demonstrates mutual exclusion using CriticalSection class.
    Creates competing threads attempting to enter protected code sections.
    """
    # Section header for output clarity
    print("\n===== CRITICAL SECTION DEMONSTRATION =====")
    
    # Instantiate synchronization mechanism
    cs = criticalSection()
    
    # List to track created threads
    threads = []
    
    # Thread creation with clear identifiers
    # Range(1,2) creates 1 thread - modify range(1,N) for more threads
    for i in range(1, 2):
        # Create thread with meaningful name for logging
        t = threading.Thread(
            name=f"CSThread-{i}",  # Unique thread identifier
            # Lambda captures current i value for process ID
            target=lambda pid=i: cs.critical_section(str(pid))
        )
        threads.append(t)
        # Log thread creation event
        print(f"[{time.strftime('%H:%M:%S')}] Created thread for Process {i}")
    
    # Thread execution phase
    for i, t in enumerate(threads, 1):  # Start enumeration at 1 for readability
        # Log thread start
        print(f"[{time.strftime('%H:%M:%S')}] Starting thread for Process {i}")
        t.start()  # Begin thread execution
        
        # Intentional delay for two reasons:
        # 1. Simulate staggered process starts
        # 2. Make console output more readable
        time.sleep(0.2)
    
    # Thread cleanup phase
    for i, t in enumerate(threads, 1):
        t.join()  # Block until thread completes
        print(f"[{time.strftime('%H:%M:%S')}] Process {i} thread completed")
    
    # Section footer for output structure
    print("===== CRITICAL SECTION DEMONSTRATION COMPLETE =====\n")

def test_bounded_buffer():
    """
    Demonstrates producer-consumer pattern using BoundedBuffer class.
    Shows coordination between resource producers and consumers.
    """
    print("\n===== BOUNDED BUFFER DEMONSTRATION =====")
    
    # Configuration with small buffer to quickly demonstrate waiting
    buffer_size = 3  # Try increasing to see different behavior
    bb = BoundedBuffer(buffer_size)
    
    # Producer function definition
    def producer_func():
        # Generate 1 item (modify range for more productions)
        for i in range(1, 2):
            item_name = f"Item-{i}"
            bb.produce(item_name)  # Add item to buffer
            
            # Simulate real-world production variance
            delay = random.uniform(0.5, 1.5)  # Random wait between 0.5-1.5 seconds
            print(f"[{time.strftime('%H:%M:%S')}] Producer sleeping for {delay:.2f} seconds")
            time.sleep(delay)
    
    # Consumer function definition        
    def consumer_func():
        # Consume 1 item (modify range for more consumptions)
        for i in range(1, 2):
            bb.consume()  # Remove item from buffer
            
            # Simulate real-world consumption variance
            delay = random.uniform(0.7, 2.0)  # Random wait between 0.7-2 seconds
            print(f"[{time.strftime('%H:%M:%S')}] Consumer sleeping for {delay:.2f} seconds")
            time.sleep(delay)
    
    # Thread creation with descriptive names
    producer_thread = threading.Thread(name="Producer-1", target=producer_func)
    consumer_thread = threading.Thread(name="Consumer-1", target=consumer_func)
    
    # Start producer first
    print(f"[{time.strftime('%H:%M:%S')}] Starting producer thread")
    producer_thread.start()
    
    # Delay consumer start to:
    # 1. Let buffer accumulate some items
    # 2. Demonstrate consumer waiting when buffer empty
    time.sleep(1.5)
    print(f"[{time.strftime('%H:%M:%S')}] Starting consumer thread")
    consumer_thread.start()
    
    # Wait for producer completion
    producer_thread.join()
    print(f"[{time.strftime('%H:%M:%S')}] Producer thread completed")
    
    # Wait for consumer completion
    consumer_thread.join()
    print(f"[{time.strftime('%H:%M:%S')}] Consumer thread completed")
    
    print("===== BOUNDED BUFFER DEMONSTRATION COMPLETE =====\n")

# Main execution block
if __name__ == "__main__":
    #print("Starting Synchronization Demonstrations")
    
    # Run critical section test first
    #test_critical_section()
    
    # Buffer between demonstrations
    print("\nWaiting 3 seconds before starting the bounded buffer test...\n")
    time.sleep(3)  # Pause for output readability
    
    # Run producer-consumer test
    test_bounded_buffer()
    
    # Final program status
    print("\nAll demonstrations completed")