from collections import defaultdict, deque

def fifo(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    cur_page_pos = 0
    history = []
    
    for page in pages:
        if page not in page_frame:
            page_frame[cur_page_pos] = page
            page_faults += 1
            cur_page_pos = (cur_page_pos + 1) % frame_size
        
        history.append(page_frame.copy())
    
    return page_faults, history

def opt(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    indices_list = defaultdict(deque)

    for i in range(len(pages)):
        indices_list[pages[i]].append(i)

    for i in range(len(pages)):
        indices_list[pages[i]].popleft()
        if pages[i] not in page_frame:
            replace_index, max_distance = -1, -1
            for j in range(len(page_frame)):
                if page_frame[j] == None or len(indices_list[page_frame[j]]) == 0:
                    replace_index, max_distance = j, -1
                    break

                if max_distance < indices_list[page_frame[j]][0]:
                    replace_index, max_distance = j, indices_list[page_frame[j]][0]

            page_frame[replace_index] = pages[i]
            page_faults += 1
        
        history.append(page_frame.copy())

    return page_faults, history

def lru(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    recently_used_queue = deque([])

    for page in pages:
        if page in page_frame:
            recently_used_queue.remove(page)
            recently_used_queue.append(page)
        else:
            in_queue = False
            for i in range(len(page_frame)):
                if page_frame[i] == None:
                    page_frame[i] = page
                    recently_used_queue.append(page)
                    in_queue = True
                    break

            if not in_queue:
                lru_page = recently_used_queue.popleft()
                page_frame[page_frame.index(lru_page)] = page

                recently_used_queue.append(page)

            page_faults += 1

        history.append(page_frame.copy())
    return page_faults, history

def mru(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    recently_used_queue = deque([])

    for page in pages:
        if page in page_frame:
            recently_used_queue.remove(page)
            recently_used_queue.append(page)
        else:
            in_queue = False
            for i in range(len(page_frame)):
                if page_frame[i] == None:
                    page_frame[i] = page
                    recently_used_queue.append(page)
                    in_queue = True
                    break

            if not in_queue:
                mru_page = recently_used_queue.pop()
                page_frame[page_frame.index(mru_page)] = page

                recently_used_queue.append(page)

            page_faults += 1

        history.append(page_frame.copy())
    return page_faults, history

def lfu(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    use_count = defaultdict(int)
    recently_used_queue = deque([])

    for page in pages:
        if page in page_frame:
            recently_used_queue.remove(page)
            recently_used_queue.append(page)
        else:
            in_queue = False
            for i in range(len(page_frame)):
                if page_frame[i] == None:
                    page_frame[i] = page
                    recently_used_queue.append(page)
                    in_queue = True
                    break

            if not in_queue:
                replaced_page, count = -1, 100000

                # Find LFU page. If there are more than 2 pages with the same count, consider LRU
                for page_in_queue in recently_used_queue:
                    if use_count[page_in_queue] < count:
                        replaced_page, count = page_in_queue, use_count[page_in_queue]
                
                recently_used_queue.remove(replaced_page)
                page_frame[page_frame.index(replaced_page)] = page

                recently_used_queue.append(page)

            page_faults += 1

        if page in use_count:
            use_count[page] += 1
        else:
            use_count[page] = 1

        history.append(page_frame.copy())
    return page_faults, history

def mfu(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    use_count = defaultdict(int)
    recently_used_queue = deque([])

    for page in pages:
        if page in page_frame:
            recently_used_queue.remove(page)
            recently_used_queue.append(page)
        else:
            in_queue = False
            for i in range(len(page_frame)):
                if page_frame[i] == None:
                    page_frame[i] = page
                    recently_used_queue.append(page)
                    in_queue = True
                    break

            if not in_queue:
                replaced_page, count = -1, -1

                # Find MFU page. If there are more than 2 pages with the same count, consider LRU
                for page_in_queue in recently_used_queue:
                    if use_count[page_in_queue] > count:
                        replaced_page, count = page_in_queue, use_count[page_in_queue]
                
                recently_used_queue.remove(replaced_page)
                page_frame[page_frame.index(replaced_page)] = page

                recently_used_queue.append(page)

            page_faults += 1

        if page in use_count:
            use_count[page] += 1
        else:
            use_count[page] = 1

        history.append(page_frame.copy())
    return page_faults, history

def second_chance(pages, frame_size):
    page_frame = [None] * frame_size
    page_faults = 0
    history = []

    ref_bit = defaultdict(int)
    recently_used_queue = deque([])

    for page in pages:
        if page in page_frame:
            recently_used_queue.remove(page)
            recently_used_queue.append(page)
            ref_bit[page] = 1
        else:
            in_queue = False
            for i in range(len(page_frame)):
                if page_frame[i] == None:
                    page_frame[i] = page
                    recently_used_queue.append(page)
                    in_queue = True
                    break

            if not in_queue:
                replaced_page = -1

                # Find page with ref. bit = 0
                for page_in_queue in recently_used_queue:
                    if ref_bit[page_in_queue] == 1:
                        ref_bit[page_in_queue] = 0
                    else:
                        replaced_page = page_in_queue
                        break

                # If all ref. bit == 1, take the LRU page
                if replaced_page == -1:
                    replaced_page = recently_used_queue.popleft()
                else:
                    recently_used_queue.remove(replaced_page)

                page_frame[page_frame.index(replaced_page)] = page

                recently_used_queue.append(page)

            page_faults += 1

        ref_bit[page] = 1
        history.append(page_frame.copy())
        print(recently_used_queue)
        print(ref_bit)
    return page_faults, history
