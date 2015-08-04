This SPEC is unfinished! Do not use in its current state.

#Build Steps

* Enable EPEL repo from https://fedoraproject.org/wiki/EPEL
* Install the build dependencies.
* Download source of Virtualbox e.g. 4.3.30 i.e. `wget http://download.virtualbox.org/virtualbox/4.3.30/VirtualBox-4.3.30.tar.bz2`
* Uncompress the *.tar.bz2 file
* run `./configure --disable-docs`
* source ./env.sh
* kmk
