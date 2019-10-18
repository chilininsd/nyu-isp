if "testfile.txt.a" in listfiles():
  removefile("testfile.txt.a")
if "testfile.txt.b" in listfiles():
  removefile("testfile.txt.b")

# create flow
try:
  myfile=ABopenfile("testfile.txt",True)  #Create an AB file
  assert('SE' == myfile.readat(None,0))
  myfile.writeat("Stest12345E",0)
  assert('SE' == myfile.readat(None,0))
  myfile.close()
  myfile=ABopenfile("testfile.txt",False)
  assert('Stest12345E' == myfile.readat(None,0))
  myfile.close()
except:
  myfile.close()
  log("Exception in create flow\n")

# append flow
try:
  myfile = ABopenfile("testfile.txt", False)
  assert("Stest12345E" == myfile.readat(None, 0))
  myfile.writeat("bar", 0)
  assert("Stest12345E" == myfile.readat(None, 0))
  myfile.close()
  myfile = ABopenfile("testfile.txt", False)
  contents = myfile.readat(None, 0)
  assert(contents == "Stest12345E")
  myfile.close()
except:
  log("Exception in append flow\n")
  myfile.close()

# re-open flow
try:
  myfile = ABopenfile("testfile.txt", True)
  assert("SE" == myfile.readat(None, 0))
  myfile.writeat("", 0)
  assert("SE" == myfile.readat(None, 0))
  myfile.close()
  myfile = ABopenfile("testfile.txt", False)
  content = myfile.readat(None, 0)
  assert(content == "SE")
  myfile.close()
except:
  myfile.close()
  log("Exception in re-open flow\n")

# .a deleted flow
try:
  myfile = ABopenfile("testfile.txt", True)
  myfile.writeat("SdeletedE", 0)
  myfile.close()
  removefile("testfile.txt.a")
  myfile = ABopenfile("testfile.txt", False)
  assert("SdeletedE" == myfile.readat(None, 0))
  myfile.close()
except:
  myfile.close()
  log("Exception in .a deleted flow")
