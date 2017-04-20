#importing python libraries
import threading,socket,re,select


#define network variables
s = socket.socket()# Create a socket object
host = "192.168.0.107" #define host
port = 8215
s.bind((host, port))        # Bind to the port
max_connections = 5
s.listen(max_connections)   #allow only 5 clients to connect



#define other variable
largest = 0 
clients = []
outfromc = []
ids = []
primes = []


#independent thread that looks for new clients trying to connect and allows them to connect.
def createcon():
    global clients,s #globalize client array and s which is the socket object
    
    while 1:
        c, addr = s.accept() #if there is a connected stick the clients addres in the addr variable and the c to data address associated with that client connection 
        print(c)

        clients.append(c) #stick client info into clients array
        print(clients)
        
        print("new connection from " + str(addr))



#if one client sends multiple messages(the can contain anything) 
def orderc(com,id1):
    global outfromc,ids
    #print("orderc")
    let = ""
    for i in range(len(com)): #iterate though incoming strings
        char = com[i] #set 
        let = let + char #build new packet
        if char == ";": #test for end of packet
            
            ids.append(id1) #return addres of packet
            outfromc.append(let) #contents of packet
            let = "" #reset packet builder

            

    
#function that can receive data from all clients and then sends the data off to be ordered    
def read(): 
    global clients
    
   # print("on")
    out = ""
    for i in range(len(clients)): #iterate though list of clients
      c = clients[i]
      c.settimeout(.1) #if client does not send full 1024 bytes move along after .1 seconds
      try:
          coms = c.recv(1024)
          
          if len(coms) >0:
              #print(coms)
              orderc(coms,c)
      except:
            pass


#function that encodes two inputs into a string that can be sent to the server or client
def enc(head,body):
  return("." + str(head) + "," + str(body) + ";") # format data so it can be send to client


#function that takes an input of an encoded string and decodes it into a head and body  
def dec(cont): #opposite of enc function
  #print(cont)
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
  #print(head,body)
  return(head,body)



#function that generates new range of numbers to be tested  and sends them to be tested
def sendn(id1):
    global largest #largest is the largest number we have tested so far
    sm = largest + 1
    la = largest + 50 #defines largest number that will be tested
    largest = largest + 50
    id1.send(enc("tr",(str(sm) + "," + str(la)))) #sends a chunk of la-sm numbers that will be tested by the client


    
#function that reads the list of stuff sent from client and acts upon what is sent
def readcoms():
    global outfromc,ids,primes
    for i in range(len(outfromc)):
        cur =  outfromc[i]#set var cur to a single element in outfromc so view it
        fnc = dec(cur) #decode that packet
        if fnc[0] == "complete":
            sendn(ids[i])
            
            #print("found new request")
        if fnc[0] == "primes":
            cont = fnc[1]
            if len(cont) > 2:
               # print(cont,fnc[1],fnc[0])
                cont=cont.strip("]")
                cont=cont.strip("[")
                #print(cont)
                cont = cont.split(",")
                cont = map(int,cont)
                primes = primes + cont
                
        
    ids = []
    outfromc = []
    


            


        
        
    


res = threading.Thread(target=createcon)
res.start()
while 1:
    read()
    readcoms()
    #if len(outfromc) > 0:
       # print(outfromc)
    #if largest != 0:
        #print(largest)
    if len(primes) >0:
        print(primes[len(primes)-1])
        #print("\n"*30)
