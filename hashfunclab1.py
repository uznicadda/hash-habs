from ripemd320lab1 import ripemd320
import time
import string
import random

def preimage_1(original_message, printmsg=False, fi=None):
    full_hash_original = ripemd320(original_message)
    target_hash = full_hash_original[-4:]
    
    if printmsg:
        print("\n--- Випадковий пошук прообразу: варіант 1 ---", file=fi)
        print(f"Оригінальне повідомлення: '{original_message}'", file=fi)
        print(f"Повний геш: {full_hash_original}", file=fi)
        print(f"Усічений геш (16 біт): {target_hash}", file=fi)
    
    counter = 0
    start_time = time.time()
    
    while True:
        modified_message = f"{original_message}{counter+1}"
        
        current_full_hash = ripemd320(modified_message)
        current_truncated_hash = current_full_hash[-4:]

        if printmsg:
            if counter < 30:
                print(f"[{counter + 1}] Повідомлення: '{modified_message}' | Геш: {current_full_hash}", file=fi)
        
        if current_truncated_hash == target_hash:
            end_time = time.time()
            if printmsg:
                print("\nПрообраз знайдено:", file=fi)
                print(f"Підібране повідомлення: '{modified_message}'", file=fi)
                print(f"Повний RIPEMD320: {current_full_hash}", file=fi)
                print(f"Усічений геш: {current_truncated_hash}", file=fi)
                print(f"Кількість спроб: {counter + 1}", file=fi)
                print(f"Час: {end_time - start_time:.4f} секунд", file=fi)
            return counter
            
        counter += 1


def preimage_2(original_message, printmsg=False, fi=None):
    full_hash_original = ripemd320(original_message)
    target_hash = full_hash_original[-4:]

    if printmsg:
        print("\n--- Випадковий пошук прообразу: варіант 2 ---", file=fi)
        print(f"Оригінальне повідомлення: '{original_message}'", file=fi)
        print(f"Повний геш: '{full_hash_original}'", file=fi)
        print(f"Усічений геш (16 біт): {target_hash}", file=fi)
    
    charset = string.ascii_lowercase + string.digits
    counter = 0
    start_time = time.time()
    
    while True:
        msg_list = list(original_message)
        num_replacements = random.randint(1, len(original_message))
        indices_to_replace = random.sample(range(len(original_message)), num_replacements)
        
        for idx in indices_to_replace:
            msg_list[idx] = random.choice(charset)
            
        modified_message = "".join(msg_list)
        
        if modified_message == original_message:
            continue
            
        current_full_hash = ripemd320(modified_message)
        current_truncated_hash = current_full_hash[-4:]
        
        if printmsg:
            if counter < 30:
                print(f"[{counter + 1}] Повідомлення: '{modified_message}' | Геш: {current_full_hash}", file=fi)
        
        if current_truncated_hash == target_hash:
            end_time = time.time()
            if printmsg:
                print("\nПрообраз знайдено:", file=fi)
                print(f"Підібране повідомлення: '{modified_message}'", file=fi)
                print(f"Повний RIPEMD320: {current_full_hash}", file=fi)
                print(f"Усічений геш (16 біт): {current_truncated_hash}", file=fi)
                print(f"Кількість спроб: {counter}", file=fi)
                print(f"Час: {end_time - start_time:.4f} секунд", file=fi)
            return counter
            
        counter += 1
        
def collision_1(original_message, printmsg=False, fi=None):
    seen_hashes = {}
    full_hash_original = ripemd320(original_message)
    target_hash = full_hash_original[-8:]
    seen_hashes[target_hash] = original_message
    if printmsg:
        print("\n--- Випадковий пошук колізії: варіант 1 ---", file=fi)
        print(f"Оригінальне повідомлення: '{original_message}'", file=fi)
        print(f"Повний геш: {full_hash_original}", file=fi)
        print(f"Усічений геш (32 біт): {target_hash}", file=fi)
    
    counter = 0
    start_time = time.time()
    
    while True:
        current_message = f"{original_message}{counter+1}"
        full_hash = ripemd320(current_message)
        truncated_hash = full_hash[-8:]

        if printmsg:
            if counter < 30:
                print(f"[{counter + 1}] Повідомлення: '{current_message}' | Геш: {full_hash}", file=fi)
        
        if truncated_hash in seen_hashes and current_message != seen_hashes[truncated_hash]:
            end_time = time.time()
            
            colliding_message = seen_hashes[truncated_hash]
            if printmsg:
                print("\nКолізія знайдена:", file=fi)
                print(f"Повідомлення 1: '{colliding_message}'", file=fi)
                print(f"Повідомлення 2: '{current_message}'", file=fi)
                print(f"Усічений геш (32 біт): {truncated_hash}", file=fi)
                
                full_hash_1 = ripemd320(colliding_message)
                print(f"Повний RIPEMD320 1: {full_hash_1}", file=fi)
                print(f"Повний RIPEMD320 2: {full_hash}", file=fi)
                
                print(f"\nКількість спроб: {counter + 1}", file=fi)
                print(f"Час: {end_time - start_time:.2f} секунд", file=fi)
            return counter
            
        seen_hashes[truncated_hash] = current_message
        counter += 1


def collision_2(original_message, printmsg=False, fi=None):
    full_hash_original = ripemd320(original_message)
    target_hash = full_hash_original[-8:]
    seen_hashes = {}
    seen_hashes[target_hash] = original_message
    
    if printmsg:
        print("\n--- Випадковий пошук колізії: варіант 2 ---", file=fi)
        print(f"Оригінальне повідомлення: '{original_message}'", file=fi)
        print(f"Повний геш: {full_hash_original}", file=fi)
        print(f"Усічений геш (32 біт): {target_hash}", file=fi)
    
    counter = 0
    start_time = time.time()
    charset = string.ascii_lowercase + string.digits
    
    
    while True:
        msg_list = list(original_message)
        num_replacements = random.randint(1, len(original_message))
        indices_to_replace = random.sample(range(len(original_message)), num_replacements)
        
        for idx in indices_to_replace:
            msg_list[idx] = random.choice(charset)
            
        modified_message = "".join(msg_list)
        
        if modified_message == original_message:
            continue
        
        full_hash = ripemd320(modified_message)
        truncated_hash = full_hash[-8:]

        if printmsg:
            if counter < 30:
                print(f"[{counter + 1}] Повідомлення: '{modified_message}' | Геш: {full_hash}", file=fi)
        
        if truncated_hash in seen_hashes and modified_message != seen_hashes[truncated_hash]:
            end_time = time.time()
            
            colliding_message = seen_hashes[truncated_hash]
            if printmsg:
                print("\nКолізія знайдена:", file=fi)
                print(f"Повідомлення 1: '{colliding_message}'", file=fi)
                print(f"Повідомлення 2: '{modified_message}'", file=fi)
                print(f"Усічений геш (32 біт): {truncated_hash}", file=fi)
                
                full_hash_1 = ripemd320(colliding_message)
                print(f"Повний RIPEMD320 1: {full_hash_1}", file=fi)
                print(f"Повний RIPEMD320 2: {full_hash}", file=fi)
                
                print(f"\nКількість спроб: {counter + 1}", file=fi)
                print(f"Час: {end_time - start_time:.2f} секунд", file=fi)
            return counter
            
        seen_hashes[truncated_hash] = modified_message
        counter += 1
        
