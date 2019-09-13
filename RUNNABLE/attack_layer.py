def dump(name):
    file = openfile(name, False)
    content = file.readat(None, 0)
    file.close()
    return content

if "testfile.txt.a" in listfiles():
  removefile("testfile.txt.a")
if "testfile.txt.b" in listfiles():
  removefile("testfile.txt.b")

# locked
myfile=ABopenfile("testfile.txt",True)  #Create an AB file
assert('SE' == myfile.readat(None,0))
myfile.writeat("Stest12345E",0)
assert('SE' == myfile.readat(None,0))
myfile.close()
assert(dump("testfile.txt.a") == dump("testfile.txt.b"))
# locked


