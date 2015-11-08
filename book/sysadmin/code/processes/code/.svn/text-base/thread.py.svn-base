import thread

def child(tid):
    print "hello from thread", tid

def parent():
    i = 0
    while 1:
        i = i+1
        thread.start_new(child, (i,))
        if raw_input() == '1': break

parent()
