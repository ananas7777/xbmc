import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time

ADDON = xbmcaddon.Addon(id='plugin.video.keywordinstaller')


def loglocation(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        log = os.path.join(log_path, 'xbmc.log')
    return log_path


def CATEGORIES():
    log_path=loglocation()
    log = os.path.join(log_path, 'xbmc.log')
    logfile=open(log, 'r').read()
    
    if 'JSONRPC: Incoming request: {"jsonrpc": "2.0","id": 0,"method": "Addons.ExecuteAddon","params": {"addonid": "plugin.video.keywordinstaller"' in logfile:
        match=re.compile('"params": {"mode": "2","url": "(.+?)"').findall(logfile)
        dialog = xbmcgui.Dialog()
        import time
        path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib          =  os.path.join(path, 'my_url_installer.zip')
        addonfolder  =  xbmc.translatePath(os.path.join('special://home/addons',''))
        DownloaderClass(match[0],lib)
        time.sleep(3)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)" %(lib,addonfolder))
        dialog.ok("URl Installer", "All Done","Next Time You Reboot Will Take Effect", "[COLOR yellow]Brought To You By TLBB[/COLOR]")
    else:
	    
        dialog = xbmcgui.Dialog()
        import time
        url      =  SEARCH()
        path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib          =  os.path.join(path, 'my_url_installer.zip')
        addonfolder  =  xbmc.translatePath(os.path.join('special://home/addons',''))
        
        DownloaderClass(url,lib)
        time.sleep(3)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)" %(lib,addonfolder))
        dialog.ok("URl Installer", "All Done","Next Time You Reboot Will Take Effect", "[COLOR yellow]Brought To You By TLBB[/COLOR]")
	        
def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Keyword')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  'http://bit.ly/tlbb' + keyboard.getText() .replace(' ','%20')  # sometimes you need to replace spaces with + or %20
            #search_entered = str.join( 'http://bit.ly/',search_entered )
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
    
    
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Keyword Installer","Downloading & Copying File",'')
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()
    
    
    
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
