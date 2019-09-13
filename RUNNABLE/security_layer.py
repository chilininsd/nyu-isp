"""
This security layer inadequately handles A/B storage for files in RepyV2.



Note:
    This security layer uses encasementlib.r2py, restrictions.default, repy.py and Python
    Also you need to give it an application to run.
    python repy.py restrictions.default encasementlib.r2py [security_layer].r2py [attack_program].r2py 
    
    """ 
TYPE="type"
ARGS="args"
RETURN="return"
EXCP="exceptions"
TARGET="target"
FUNC="func"
OBJC="objc"

"""
goals:
    1. .b is always an exact copy of .a
    2. file always starts with S and ends with E
    3. protect my backup file
"""

class ABFile():
    def __init__(self,filename,create):
        # globals
        mycontext['debug'] = True   
        # local (per object) reference to the underlying file
        self.Afn = filename+'.a'
        self.Bfn = filename+'.b'

        # make the files and add 'SE' to the readat file...
        if create:
            self.Afile = openfile(self.Afn,create)
            self.Bfile = openfile(self.Bfn,create)
            self.Afile.writeat('SE',0)
            self.diag("postcreate")
        else:
            files = listfiles()
            if files.index(self.Afn) > 0:
                self.Afile = openfile(self.Afn, False)
            if files.index(self.Bfn) > 0:
                self.Bfile = openfile(self.Bfn, False)


    def writeat(self,data,offset):
        self.diag("write-before")
        self.Bfile.writeat(data,offset)
        self.diag("write-after")
  
    def readat(self,bytes,offset):
        if self.isValid(self.Afile):
            contents = self.Afile.readat(bytes, offset)
            self.diag("security: readat")
            return contents
        return ""

#FIXME: need to lock, I think that's the only way to truly prevent these issues.
    def close(self):
        copied = self.copyFileToFileIfValid(self.Bfile, self.Afile)
        if not copied:
            self.copyFileToFileIfValid(self.Afile, self.Bfile)

        self.Afile.close()
        self.Bfile.close()

    def isValid(self, file):
        fileContents = file.readat(None,0)
        if fileContents is not None and len(fileContents) > 0:
            firstChar = fileContents[0]
            lastChar = fileContents[-1]
            self.diag("security: isValid", firstChar, lastChar)
            return firstChar == 'S' and lastChar == 'E'

    def copyFileToFileIfValid(self, fileToCopyFrom, fileToCopyTo):
        if self.isValid(fileToCopyFrom):
            fileContents = fileToCopyFrom.readat(None,0)
            fileToCopyTo.writeat(fileContents, 0)
            return True
        else:
            return False

    def diag(self, message, *argv):
        if mycontext.get("debug") == True:
            gDiag(message, argv)
            log("\tA file = " + self.Afile.readat(None,0))
            log("\n")
            log("\tB file = " + self.Bfile.readat(None,0))
            log("\n")

def ABopenfile(filename, create):
    return ABFile(filename,create)

def gDiag(message, *argv):
    log(message)
    log("\n")
    for arg in argv:
        if arg is not None:
            log("\t" + str(arg))
            log("\n")

# The code here sets up type checking and variable hiding for you.  You
# should not need to change anything below here.
sec_file_def = {"obj-type":ABFile,
                "name":"ABFile",
                "writeat":{"type":"func","args":(str,(int,long)),"exceptions":Exception,"return":(int,type(None)),"target":ABFile.writeat},
                "readat":{"type":"func","args":((int,long,type(None)),(int,long)),"exceptions":Exception,"return":str,"target":ABFile.readat},
                "close":{"type":"func","args":None,"exceptions":None,"return":(bool,type(None)),"target":ABFile.close}
           }

CHILD_CONTEXT_DEF["ABopenfile"] = {TYPE:OBJC,ARGS:(str,bool),EXCP:Exception,RETURN:sec_file_def,TARGET:ABopenfile}

# Execute the user code
secure_dispatch_module()