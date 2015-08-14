#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web, json, os, sys

def log(s):
    sys.stderr.write("%s\n" % s)

urls = (
    '/smartpro123', 'index',
    '/upload3434', 'upload',
    '/control3434', 'control'
)

templatePath = "/home/pi/Desktop/server/templates/"
path = "/home/pi/files/"
pipePath = "/home/pi/dosya"

render = web.template.render(templatePath)
app = web.application(urls, globals())

class index:
    def GET(self):
        return render.index()

    def POST(self):
        pass

class control:
    def GET(self):
        i = web.input(comm = "")
        if i.comm != "":
            data = web.websafe(i.comm)
            
            senderIp = web.ctx.ip # sayfayı ziyaret kişinin adresi
            log("data degismedi : " + data)
            data = "%s%s%s" %(data, " ", senderIp)

            log("data : " + data)
            fout = open(pipePath, 'w')
            fout.write(data)
            fout.close

        return render.control(function = {'createInputForm' : self.createInputForm(), 'createKeyForm' : self.createKeyForm()})

    def getFiles(self): #Dosyalarin saklandigi konuma bakip orada bulunan butun dosya isimleri ve uzantıları saklar
        files = os.listdir(path) # path konumundaki butun dosya isimlerini bir listede tutar
        filesAndExt = []
        for name in files: # dosya isimleri '.' ya göre parcalar ve bunları bir liste icine [["resim", "png"], ["video", "mp4"]] seklinde saklar
            fileExt = name.split('.')
            filesAndExt.append([fileExt[0], fileExt[1]])
        return filesAndExt

    def createInputForm(self): # form input yapisini dosya isimlerini value olarak ayarlayip olusturuyor
        filesAndExt = self.getFiles()
        value = ""
        inputBase = "<input type=\"radio\" name=\"comm\" "
        for x in filesAndExt:
            fullName = x[0] + "." + x[1]

            #olusturulmak istenen ornek yapi
            #<input type="radio" name="comm" value="ornek.png"> ornek.png <br>
            if x[1] == "png":
                value = "%s%s%s%s%s%s%s" %(value, inputBase, "value=\"", fullName, "\" >", fullName, "<br>\n") 
            elif x[1] == "mp4" or x[1] == "mkv":
                value = "%s%s%s%s%s%s%s" %(value, inputBase, "value=\"", fullName, "\" >", fullName, "<br>\n")
            elif x[1] == "pdf":
                value = "%s%s%s%s%s%s%s" %(value, inputBase, "value=\"", fullName, "\" >", fullName, "<br>\n")
        return value

    def createKeyForm(self):
        return "createKeyForm"

class upload:
    def GET(self):

        i = web.input(upload = "")
        data1 = web.websafe(i.upload)

        return render.upload(data1)

    def POST(self):
        x = web.webapi.rawinput().get("myfile")
        fname = None

        if not os.path.isdir(path): #dosyalarin kaydedilecegi bolumun var olup olmadıgının kontrolu eger yoksa olustur
            os.mkdir(path, 0755)

        #tek dosya gelirse tekli listeye cevriliyor
        if not isinstance(x, list):
            x = [x]

        for nFile in x:
            filepath=nFile.filename #.replace('\\','/') # replaces the windows-style slashes with linux ones.
            print filepath
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            print filename
            #fout = open(path +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            fname = "%s%s" %(path, filename)
            fout = open(fname, 'w') 
            fout.write(nFile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        if isinstance(x, list):
            successList = []
            for i in x:
                if os.path.exists(path + i.filename):
                    successList.append(i.filename + '  ')

            raise web.seeother('/upload3434?upload=' + ''.join(successList)) # ''.join ile stringe donusturuyor
        else:
            raise web.seeother('/upload3434?upload=Basarisiz')

def main():
    app.run()

if __name__ == "__main__":
    main()
