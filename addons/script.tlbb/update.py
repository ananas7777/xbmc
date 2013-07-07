#
#      Copyright (C) 2013 Sean Poyser
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc
import os

import urllib2
import urllib
import json

import utils


def checkForUpdate(silent = 1):

    if silent == '2' or silent=='3':
        utils.rebootCommand(silent)
        return
           
    utils.saveOta()
    silent = int(silent) == 1

    if silent and utils.getSetting('autoUpdate') == 'false':
        return allDone(silent)

    response = getResponse()
    isValid  = len(response) > 0

    if not isValid:
        if not silent:
            utils.ok(1, 12, 13)
        return allDone(silent)
   
    if updateAvailable(response['Version']):
        utils.log('Update Available')
        performUpdate(response, silent)    
    elif not silent:
        if downloaded():
            checkPrevious()
        else:
            utils.ok(1, 22, 13)

    allDone(silent)


def allDone(silent, mins = 10080):
    setAlarm(mins)

    if not silent:
        utils.ADDON.openSettings() 


def setAlarm(mins):
    #set script to run again in x minutes

    updateMins = mins
    addonPath  = utils.getAddonPath(False)
    name       = 'TLBB Update'
    script     = os.path.join(addonPath, 'update.py')
    args       = '1' #silent
    cmd        = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, updateMins)

    xbmc.executebuiltin('CancelAlarm(%s,True)' % name)        
    xbmc.executebuiltin(cmd)


def getResponse():
    try:
        url      = 'http://www.thelittleblackbox.nl/ota.php'
        response = urllib2.urlopen(url).read()
    except:
        return []
    
    return json.loads(u"" + (response))


def updateAvailable(latest):
    current = utils.getSetting('cVersion')
    current = current.split('.')
    latest  = latest.split('.')

    length  = min(len(current), len(latest))

    for i in range(0, length):
        if int(latest[i]) > int(current[i]):
            utils.flagUpdate()
            return True

    return False


def performUpdate(response, silent):
    try:
        version = response['Version']
        link    = response['Link']
        md5     = response['MD5']
    except:
        return

    path = getDownloadPath()

    if utils.generateMD5(path) != md5:
        if (not silent) and (not utils.yesno(1, 10, 11)):
            return

        dp = None
    
        if not silent:
            dp = utils.progress(1, 14, 15)

        hash   = 0
        count  = 0
        nTries = 3

        if not silent:
            nTries = 1
    
        while (count < nTries) and (hash != md5):
            count += 1
            try:        
                download(link, path, dp)
                hash = utils.generateMD5(path)
            except Exception, e:
                utils.deleteFile(path)
                if str(e) == 'Canceled':                    
                    return

        if hash != md5:
            utils.unflagUpdate()
            utils.deleteFile(path)
            utils.setSetting('dVersion', '0.0.0')
            if not silent:
                utils.ok(1, 24, 13)
            return
        
    utils.setSetting('dVersion', version)

    if not utils.okReboot(1, 23, 16, 18, delay = 15):
        return

    reboot()


def reboot():
    version = utils.getSetting('dVersion') 

    utils.setSetting('cVersion', version)
    utils.setSetting('dVersion', '0.0.0')

    cmd = 'recoveryflash'

    utils.reboot(cmd)


def getDownloadPath():
    path = '/recovery/update.zip'
    return path


def downloaded():
    filename = getDownloadPath()
    return os.path.exists(filename)


def download(url, dest, version, dp = None, start = 0, range = 100):    
    if not dp:
        urllib.urlretrieve(url,dest)
    else:
        dp.update(int(start))
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,dp,start,range,url))
 

def _pbhook(numblocks, blocksize, filesize, dp, start, range, url=None):
    try:
        percent = min(start+((numblocks*blocksize*range)/filesize), start+range)
        dp.update(int(percent))
    except Exception, e:
        utils.log('%s Error Downloading Update' % str(e))
        percent = 100
        dp.update(int(percent))
    if dp.iscanceled(): 
        raise Exception('Canceled')


if __name__ == '__main__': 
    if len(sys.argv) > 1:
        checkForUpdate(sys.argv[1])
    else:
        checkForUpdate(1) #silent
