%define name oracle-ebs-server-R12-preinstall 
%define version 1.0
%define release 3.rhel7


Summary: Sets the system for Oracle  E-Business Suite Release 12 for Oracle Linux 7
Name: %{name}
Version: %{version}
Release: %{release}
Group: Test Environment/Libraries
License: GPLv2
Vendor:Oracle
Source: %{name}-%{version}.tar.gz

Provides: %{name} = %{version}

Requires(pre):/etc/redhat-release

#System requirement
Requires:procps module-init-tools ethtool initscripts 
Requires:bc bind-utils nfs-utils util-linux pam
Requires:xorg-x11-utils xorg-x11-xauth 
Requires:kernel
Requires:smartmontools
Requires:psmisc

#Common requirment 
Requires:binutils compat-libstdc++-33 gcc gcc-c++ glibc-devel 
Requires:compat-libcap1 ksh make openssh-clients sysstat util-linux

#ebiz specific
Requires:glibc-common libXp libgomp gdbm elfutils-libelf-devel perl perl-File-CheckTree redhat-lsb unzip zip

%ifarch x86_64
#64 bit versions
Requires:compat-libstdc++-33(%{__isa_name}-64)
Requires:gdbm(%{__isa_name}-64)
Requires:glibc(%{__isa_name}-64)
Requires:glibc-devel(%{__isa_name}-64)
Requires:libaio(%{__isa_name}-64)
Requires:libaio-devel(%{__isa_name}-64)
Requires:libgcc(%{__isa_name}-64)
Requires:libstdc++(%{__isa_name}-64)
Requires:libstdc++-devel(%{__isa_name}-64)
Requires:libXp(%{__isa_name}-64)
#32bit versions
Requires:compat-db47(%{__isa_name}-32)
Requires:compat-libstdc++-296(%{__isa_name}-32)
Requires:compat-libstdc++-33(%{__isa_name}-32)
Requires:gdbm(%{__isa_name}-32)
Requires:glibc(%{__isa_name}-32)
Requires:glibc-devel(%{__isa_name}-32)
Requires:libaio(%{__isa_name}-32)
Requires:libaio-devel(%{__isa_name}-32)
Requires:libgcc(%{__isa_name}-32)
Requires:libstdc++(%{__isa_name}-32)
Requires:libstdc++-devel(%{__isa_name}-32)
Requires:libXi(%{__isa_name}-32)
Requires:libXp(%{__isa_name}-32)
Requires:libXrender(%{__isa_name}-32)
Requires:libXtst(%{__isa_name}-32)
%endif


#From oss
Requires:openmotif21(%{__isa_name}-32)
Requires:xorg-x11-libs-compat

BuildRoot: %{_builddir}/%{name}-%{version}-root

%description
This package installs software packages and sets system parameters required for Oracle  E-Business Suite Release 12 for Oracle Linux Release 7
Files affected: /etc/sysctl.conf, /boot/grub/menu.lst, /etc/resolve.conf
Files added: /etc/security/limits.d/oracle-ebs-server-R12-preinstall.conf


%prep
echo RPM_BUILD_ROOT=$RPM_BUILD_ROOT
%setup -q


%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/sysconfig/%{name}
mkdir -p -m 755 $RPM_BUILD_ROOT/usr/bin
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/security/limits.d
mkdir -p -m 700 $RPM_BUILD_ROOT/var/log/%{name}/results

install -m 700 oracle-ebs-server-R12-preinstall-verify $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 700 oracle-ebs-server-R12-preinstall-verify $RPM_BUILD_ROOT/usr/bin
install -m 600 oracle-ebs-server-R12-preinstall.param $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -m 700 oracle-ebs-server-R12-preinstall-firstboot $RPM_BUILD_ROOT/etc/rc.d/init.d
touch $RPM_BUILD_ROOT/etc/security/limits.d/oracle-ebs-server-R12-preinstall.conf


ln -f -s /etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall-verify $RPM_BUILD_ROOT/usr/bin/oracle-ebs-server-R12-preinstall-verify 

%clean
rm -rf $RPM_BUILD_ROOT

%pre

if [ -f  /etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall.param ]; then 
  cp -f /etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall.param /var/log/%{name}/results/.oracle-ebs-server-R12-preinstall.param 
fi

if [ -d /etc/sysconfig/%{name} ]; then
  rm -rf /etc/sysconfig/%{name} 
fi

%post
/usr/bin/oracle-ebs-server-R12-preinstall-verify 2> /dev/null 1>&2

if ! [ -f /etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall.conf ]; then
   chkconfig --add oracle-ebs-server-R12-preinstall-firstboot
fi

%preun
if [ "$1" = "0" ] ; then # last uninstall
 chkconfig --del oracle-ebs-server-R12-preinstall-firstboot
 if [ -x /usr/bin/oracle-ebs-server-R12-preinstall-verify ]; then
   /usr/bin/oracle-ebs-server-R12-preinstall-verify -u 2> /dev/null 1>&2
 fi
fi

%postun
if [ "$1" = "0" ] ; then # last uninstall
 if [ -d /etc/sysconfig/%{name} ]; then
   rm -rf /etc/sysconfig/%{name} 
 fi
 if [ -d /var/log/%{name} ]; then
   rm -rf /var/log/%{name}
 fi
fi

%files
%defattr(-,root,root)
%doc COPYING
%config /etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall.param
%ghost /etc/security/limits.d/oracle-ebs-server-R12-preinstall.conf
/etc/sysconfig/%{name}
/etc/rc.d/init.d/oracle-ebs-server-R12-preinstall-firstboot
/etc/sysconfig/%{name}/oracle-ebs-server-R12-preinstall-verify  
/var/log/%{name}
/usr/bin/oracle-ebs-server-R12-preinstall-verify

%changelog
* Fri May 25 2018 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-3.el7]
 - Fix compat-libstdc++-33 package dependency [Orabug 28079892]
 - Add gdbm to 64 bit section
 - Removed ifarch i386 section added the compat-db47, libXi, libXtst, libXrender to 32 bit section
* Tue May 8 2018 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-2.el7]
 - Fix x86-64 arch dependent packages [Orabug 27977799]
* Thu Jan 14 2016 Vasundhara V <vasundhara.venkatasubramanian@oracle.com> [1.0-1.el7]
 - Created
