/*
 *      Copyright (C) 2012 Team XBMC
 *      http://www.xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

#include "system.h"
#include "PivosPowerSyscall.h"
#include "utils/AMLUtils.h"
#include "utils/log.h"
#include <sys/types.h>
#include <dirent.h>


CPivosPowerSyscall::CPivosPowerSyscall()
{
  if (aml_get_cputype() == 1)
  {
    m_CanPowerdown = true;
    m_CanSuspend   = false;
  }
  else
  {
    m_CanPowerdown = true;
    m_CanSuspend   = false;
  }
  m_CanHibernate = false;
  m_CanReboot    = true;

  m_OnResume  = false;
  m_OnSuspend = false;
}

bool CPivosPowerSyscall::Powerdown()
{
  return true;
}

bool CPivosPowerSyscall::Suspend()
{
  m_OnSuspend = true;
  return true;
}

bool CPivosPowerSyscall::Hibernate()
{
  return false;
}

bool CPivosPowerSyscall::Reboot()
{
  return true;
}

bool CPivosPowerSyscall::CanPowerdown()
{
  return m_CanPowerdown;
}

bool CPivosPowerSyscall::CanSuspend()
{
  return m_CanSuspend;
}

bool CPivosPowerSyscall::CanHibernate()
{
  return m_CanHibernate;
}

bool CPivosPowerSyscall::CanReboot()
{
  return m_CanReboot;
}

int CPivosPowerSyscall::BatteryLevel()
{
  return 0;
}

bool CPivosPowerSyscall::PumpPowerEvents(IPowerEventsCallback *callback)
{
  if (m_OnSuspend)
  {
    // do the CPowerManager::OnSleep() callback
    callback->OnSleep();
    m_OnResume  = true;
    m_OnSuspend = false;
    // wait for all our threads to do their thing
    usleep(1 * 1000 * 1000);

    // Synchronize file system
    std::string cmd;
    cmd = "sync";
    system(cmd.c_str());

    // FIXME--------------
    // In hindsight this shouldn't be done here, as its to static
    // Should move shutdown (umount, etc) to an external script
    // Then build a script to handle remounting on resume.
    // FIXME--------------

    // Dismount all usb drives
    DIR           *d;
    struct dirent *dir;
    char  * device_path;
    d = opendir("/dev/disk/by-path");
    

    if (d)
    {
    CLog::Log(LOGINFO, "Suspending: Find usb\n");
    while ((dir = readdir(d)) != NULL)
    {
      CLog::Log(LOGINFO, "Suspending: loop %s\n",dir->d_name);
      if (strncmp(dir->d_name,"usb",3) == 0)
        {
		 cmd="/dev/disk/by-path/";
		 device_path = realpath(cmd.append(dir->d_name).c_str(),NULL);
                 if (device_path != NULL)
		 {
                 CLog::Log(LOGINFO, "Suspending: umount %s\n", device_path);
                 
                 // snprintf(cmd,100,"umount %s\n",device_path);
                 cmd = "umount ";
                 cmd.append(device_path);
                 system(cmd.c_str());
		 free(device_path);
                 }
        }
    }

    closedir(d);
    }

    // Sleep
    aml_set_sysfs_str("/sys/power/state", "mem");
    usleep(100 * 1000);
  }
  else if (m_OnResume)
  {
    // do the CPowerManager::OnWake() callback
    callback->OnWake();
    m_OnResume = false;
  }

  return true;
}

bool CPivosPowerSyscall::HasPivosPowerSyscall()
{
  return aml_present();
}
