
import queue

class Buffer(queue.Queue):
    '''
    FIFO queue to store chat data (chat components).
    If the number of stored data exceeds the max value, 
    the oldest one is discarded.

    Parameter
    ---------
    max_size : int
        Maximum number of chat blocks to store. 0 means infinite.
    '''
    def __init__(self,maxsize = 0):
        super().__init__(maxsize=maxsize)
    
    def put(self,item):
        if item is None:
            return 
        if super().full():
            super().get_nowait()
        else:
            super().put(item)
            
    def put_nowait(self,item):
        if item is None:
            return 
        if super().full():
            super().get_nowait()
        else:
            super().put_nowait(item)
            
    def get(self):
        ret = []
        ret.append(super().get())
        while not super().empty():
            ret.append(super().get())
        return ret