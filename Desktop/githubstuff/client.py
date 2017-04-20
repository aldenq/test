import socket,threading
port = 8215
host = '192.168.0.107'
dif = 0
s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
out= ""
s1.connect((host,port))
range1 = (0,0)
done1 = 1
prime = [] #primes client finds will go here


def enc(head,body):
  return("." + str(head) + "," + str(body) + ";")
#function that encodes two inputs into a string that can be sent to the server or client

def dec(cont):
  start = cont.find(".")
  mid = cont.find(",")
  end = cont.find(";")
  head = ""
  body = ""
  for i in range(len(cont)):
    if i > start and i < mid:
      head = head + cont[i]
    if i > mid and i < end:
      body = body + cont[i]
  return(head,body)
#function that takes an input of an encoded string and decodes it into a head and body

def rec(): # receive loop 
    global s1,out
    while 1:
        out = dec(s1.recv(1024)) #look for 1024 bytes from server
#function to get output from server
        
def newl():
    global range1,prime,s1
    s1.send(enc("complete",str(range1))) #tell server the range of numbers i have tested
    print("asking for new")       
    s1.send(str(enc("primes",(prime))))#send server the primes in that range
    print(enc("primes",(prime)))
    print(prime)
    prime = [] #reset prime counter so old primes will not be sent to server
    return(None)
    
#function to ask for new range of number to test for primes
    
    
test = (min(range1) if min(range1)%2 != 0 else min(range1) + 1)
#code to make starting point always odd number to avoid only testing even numbers

rec = threading.Thread(target=rec)
rec.start() #start the tried responsible for getting data from server

newl() #ask for range of numbers to test

print("made first request")
while (True):
    if len(out) > 0:
      if out[0] == "tr":
          p = out[1]
          range1 = eval(p)
            #convert range sent from server into a form that can be read by client

          print(range1)
          test = (min(range1) if min(range1)%2 != 0 else min(range1) + 1)
          done1 = 0
          out = ""
          
    if done1 == 0:
        
                
            test = test + 2
            if test < max(range1):
                
                for s in range(2,test):
                    if s > test/2:
                        #s1.send(str(test) + "\n")
                        prime.append(test)
                        print(test)
                        break
                    if test % s == 0:
                        break
            else:
                 #print("done33333333")
                 done1 = 1
                 print("completed most recent request")
                 newl()
      #tests for all primes within a range      
                 
    else:
         #print("asking for new list of number to test")
         
      
        
      pass
