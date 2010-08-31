import threading 
import time


testflag = 0

class MyThread ( threading.Thread ):
   # Override Thread's __init__ method to accept the parameters needed:
   def __init__ ( self, threadNum):

      self.threadNum = threadNum
      threading.Thread.__init__ ( self )

   def run ( self ):
      global testflag
      print "counting to 5.."
      for i in range(5):
        print "Thread Number ", self.threadNum, ' named: ',self.getName()," Count = ", i
        i = i + 1  
        time.sleep(1) 
      testflag = 1

class CheckFlag ( threading.Thread ):
   def run ( self ):
      global testflag 
      while True:
        print "checking flag.."
        time.sleep(.5)
        if testflag <> 0:
            print "flag changed"
            break


athread = MyThread(1)
athread.setName ( 'athread' )
athread.start()
time.sleep(2)
#check if thread is alive
if athread.isAlive():
   print 'athread is alive.'
else:
   print 'athread is dead'
time.sleep(3)
"""
We can use the setDaemon method, too. If a True value is passed with this method and all other threads have finished executing, the Python program will exit, leaving the thread by itself:

    import threading
    import time

    class DaemonThread ( threading.Thread ):

       def run ( self ):

          self.setDaemon ( True )
          time.sleep ( 10 )

    DaemonThread().start()
    print 'Leaving.'

Python also contains a thread module that deals with lower level threading. The only feature I would like to point out is the start_new_thread function it contains. Using this, we can turn an ordinary function into a thread:

    import thread

    def thread( stuff ):
       print "I'm a real boy!"
       print stuff

    thread.start_new_thread ( thread, ( 'Argument' ) )
"""
