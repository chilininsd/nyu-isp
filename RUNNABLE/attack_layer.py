if "testfile.txt.a" in listfiles():
  removefile("testfile.txt.a")
if "testfile.txt.b" in listfiles():
  removefile("testfile.txt.b")
log("attack: open\n")
myfile=ABopenfile("testfile.txt",True)  #Create an AB file

# I should get 'SE' when reading an empty file...
assert('SE' == myfile.readat(None,0))

log("attack: writeat\n")
# put some valid data in the file.
myfile.writeat("Stest12345E",0)

log("attack: readat\n")
# I should still get 'SE' because the file wasn't closed.
assert('SE' == myfile.readat(None,0))

log("attack: close\n")
#Close the file
myfile.close()
