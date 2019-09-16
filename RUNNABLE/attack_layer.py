def dump(name):
    file = openfile(name, False)
    content = file.readat(None, 0)
    file.close()
    return content

if "testfile.txt.a" in listfiles():
  removefile("testfile.txt.a")
if "testfile.txt.b" in listfiles():
  removefile("testfile.txt.b")

# create flow
myfile=ABopenfile("testfile.txt",True)  #Create an AB file
assert('SE' == myfile.readat(None,0))
myfile.writeat("Stest12345E",0)
assert('SE' == myfile.readat(None,0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "Stest12345E")

# append flow
myfile = ABopenfile("testfile.txt", False)
assert("Stest12345E" == myfile.readat(None, 0))
myfile.writeat("bar", 0)
assert("Stest12345E" == myfile.readat(None, 0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "Stest12345E")

# re-open flow
myobj = ABopenfile("testfile.txt", True)
assert("SE" == myobj.readat(None, 0))
myobj.writeat("", 0)
assert("SE" == myobj.readat(None, 0))
myobj.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SE")

# .a deleted flow
myfile = ABopenfile("testfile.txt", True)
myfile.writeat("SdeletedE", 0)
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SdeletedE")
removefile("testfile.txt.a")
myfile = ABopenfile("testfile.txt", False)
assert("SdeletedE" == myfile.readat(None, 0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SdeletedE")

# .a modified flow
# add modified text
myfile = ABopenfile("testfile.txt", True)
myfile.writeat("SmodifiedE", 0)
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SmodifiedE")
# modify with invalid text
backupFile = openfile("testfile.txt.a", False)
backupFile.writeat("AdeletedB", 0)
backupFile.close()
myfile = ABopenfile("testfile.txt", False)
assert("SmodifiedE" == myfile.readat(None, 0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SmodifiedE")
# modify with "valid" text
backupFile = openfile("testfile.txt.a", False)
backupFile.writeat("SmodifiedtwiceE",0)
backupFile.close()
myfile = ABopenfile("testfile.txt", False)
# this is a bug: 
assert("SmodifiedE" == myfile.readat(len("SmodifiedE"), 0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b") == "SmodifiedE")