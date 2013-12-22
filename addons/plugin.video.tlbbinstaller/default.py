import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import downloader
import extract

ADDON = xbmcaddon.Addon(id='plugin.video.tlbbinstaller')




def CATEGORIES():
        dialog = xbmcgui.Dialog()      
        dp = xbmcgui.DialogProgress()
        dp.create("Keyword Installer","Downloading ",'', 'Please Wait')
        keyword      =  SEARCH()
        url ='http://bit.ly/tlbb'+keyword
        path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib          =  os.path.join(path, keyword+'.zip')
        addonfolder  =  xbmc.translatePath(os.path.join('special://home/addons',''))
        
        downloader.download(url,lib)

        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(lib,addonfolder,dp)
        xbmc.executebuiltin('UpdateLocalAddons') 
        dialog.ok("URl Installer", "All Done","", "[COLOR yellow]Brought To You By TLBB[/COLOR]")
	        
def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Keyword')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered    
        
        
def Remote(url):
    dialog = xbmcgui.Dialog()
    import time
    path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib          =  os.path.join(path, 'my_url_installer.zip')
    addonfolder  =  xbmc.translatePath(os.path.join('special://home/addons',''))
    DownloaderClass(url,lib)
    time.sleep(3)
    xbmc.executebuiltin("XBMC.Extract(%s,%s)" %(lib,addonfolder))
    dialog.ok("Keyword Installer", "All Done","Next Time You Reboot Will Take Effect", "[COLOR yellow]Brought To You By TLBB[/COLOR]")
 
def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link
    
 
    
    
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

        
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
        
if mode==2:
        Remote(url)
       
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
