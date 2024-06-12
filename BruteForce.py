import itertools
import string
import hashlib
import threading
from queue import Queue

def check_hash(guess, target_hash):
    return hashlib.sha256(guess.encode()).hexdigest() == target_hash

def brute_force_worker(queue, target_hash, result, stop_event):
    while not queue.empty() and not stop_event.is_set():
        guess = queue.get()
        if check_hash(guess, target_hash):
            result.append(guess)
            stop_event.set()
        queue.task_done()

def brute_force_password(target_hash, max_length, num_threads=4):
    chars = string.ascii_letters + string.digits  
    queue = Queue()
    result = []
    stop_event = threading.Event()

    for length in range(1, max_length + 1):
        for guess in itertools.product(chars, repeat=length):
            queue.put(''.join(guess))

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=brute_force_worker, args=(queue, target_hash, result, stop_event))
        t.start()
        threads.append(t)

    queue.join()

    for t in threads:
        t.join()

    return result[0] if result else None

if __name__ == "__main__":
    real_password = "abc"  
    max_length = 4  
    target_hash = hashlib.sha256(real_password.encode()).hexdigest()  

    found_password = brute_force_password(target_hash, max_length, num_threads=8)
    if found_password:
        print(f"Şifre bulundu: {found_password}")
    else:
        print("Şifre bulunamadı")
