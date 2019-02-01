# Oracle EBS R12 Preinstall RPM for Redhat  ( RHEL7)

Oracle by default ship preinstall rpms for only Oracle Linux. Even though Oracle Linux is derived from Redhat Linux, we cannot install those preinstall rpms on Redhat Linux, as the rpms has prereq of using UEK kernel. So i have created new rpms for Redhat that acheive the same result using the SRPMs from oracle

You can download the rpm from below location 

https://github.com/vasuballa/oracle-rhel-preinstall/tree/master/RPMS/x86_64

Incase you want to prepare the rpm yourself, here are steps i follwed

## Here are the steps i followed

```
$ wget https://oss.oracle.com/ol7/SRPMS-updates/oracle-ebs-server-R12-preinstall-1.0-3.el7.src.rpm
$ rpm2cpio oracle-ebs-server-R12-preinstall-1.0-3.el7.src.rpm | cpio -idmv


$ mkdir -p ~/rpmbuild/SOURCES/
$ mkdir -p ~/rpmbuild/SPECS/
$ cp oracle-ebs-server-R12-preinstall-1.0.tar.gz ~/rpmbuild/SOURCES/
$ cp oracle-ebs-server-R12-preinstall.spec ~/rpmbuild/SPECS/

$ vi ~/rpmbuild/SPECS/oracle-ebs-server-R12-preinstall.spec
:%s/kernel-uek/kernel/g
:%s/3.el7/3.rhel7/g

$ rpmbuild -ba ~/rpmbuild/SPECS/oracle-ebs-server-R12-preinstall.spec
$ ls -ltr /home/oracle/rpmbuild/RPMS/x86_64/oracle-ebs-server-R12-preinstall-1.0-3.rhel7.x86_64.rpm
```
