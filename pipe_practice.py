import os

r, w = os.pipe()

# use os.fork() to create a child process - this actually makes a whole new process
# running this program, in the child process it has pid = 0, and in the parent
# process it has pid > 0 (equal to the child process id).
pid = os.fork()

if pid > 0:
    # so, if pid > 0 , we are in the PARENT process
    # We want to write something for the CHILD to read
    os.close(r)  # this is so we don't block the otherside from doing what it's doing

    print('Parent is writing')
    text = b'Hello my son'
    os.write(w, text)  # here the parent is writing "text" to the pipe
    print('Parent has written to the pipe')

if pid == 0:
    # In the other dimension, this is what the child process will run
    # We have to close the writer, so we don't block things up
    os.close(w)

    print('Child is reading')
    text = os.fdopen(r)
    print(' Child has read: ', text.read())

