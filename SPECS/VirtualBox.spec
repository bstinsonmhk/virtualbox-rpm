Name:		VirtualBox
Version:	5.0.0
Release:	1%{?dist}
Summary:	A general-purpose full virtualizer for x86 hardware

Group:		Development/Tools
License:	GPLv2
URL:		http://www.virtualbox.org
Source0:	http://download.virtualbox.org/virtualbox/%{version}/VirtualBox-%{version}.tar.bz2

BuildRequires:	gcc-c++
BuildRequires:  acpica-tools
BuildRequires:  libcap-devel 
BuildRequires:  libcurl-devel 
BuildRequires:  libIDL-devel 
BuildRequires:  libstdc++-static
BuildRequires:  libxslt-devel 
BuildRequires:  libXmu-devel 
BuildRequires:  openssl-devel 
BuildRequires:  pam-devel 
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-devel 
BuildRequires:  qt-devel 
BuildRequires:  SDL_ttf-devel 
BuildRequires:  SDL-static 
BuildRequires:  texlive-latex
BuildRequires:  device-mapper-devel 
BuildRequires:  wget subversion 
BuildRequires:  kernel-devel 
BuildRequires:  glibc-static 
BuildRequires:  zlib-static 
BuildRequires:  glibc-devel
BuildRequires:  libstdc++
BuildRequires:  libpng-devel
BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  genisoimage
BuildRequires:  libvpx-devel
BuildRequires:  makeself
BuildRequires:  libstdc++.i686
BuildRequires:  glibc-devel.i686

Requires:	    dev86 lsmod

%package devel
Summary:    Sources to build the VirtualBox kmods  

%package guest-devel
Summary:    Sources to build the VirtualBox Guest Additions kmods  

%package -n python-vboxapi
Summary:    Python bindings for VirtualBox

%description
This is a description

%description devel
The sources to build the VirtualBox host kernel modules

%description guest-devel
The sources to build the VirtualBox guest kernel modules

%description -n python-vboxapi
The python bindings to VirtualBox

%prep
%setup -q


%build
./configure --disable-kmods --disable-docs
source ./env.sh
kmk %{?_smp_mflags} PATH_OUT="`pwd`/built" \
    VBOX_PATH_APP_PRIVATE_ARCH=%{_libdir}/virtualbox \
    VBOX_PATH_APP_PRIVATE=%{_libdir}/virtualbox 

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}%{_sbindir}
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/vbox
install -m 755 -d %{buildroot}%{_datadir}/virtualbox
install -m 755 -d %{buildroot}%{_datadir}/pixmaps
install -m 755 -d %{buildroot}%{_libdir}/virtualbox
install -m 755 -d %{buildroot}%{_usrsrc}/virtualbox-kmod-%{version}/

# Main
install -p built/bin/VBoxEFI32.fd %{buildroot}%{_libdir}/virtualbox/VBoxEFI32.fd
install -p built/bin/VBoxEFI64.fd %{buildroot}%{_libdir}/virtualbox/VBoxEFI64.fd

cp -a built/bin/*.rc %{buildroot}%{_libdir}/virtualbox/
cp -a built/bin/*.r0 %{buildroot}%{_libdir}/virtualbox/

install -p built/bin/VBoxXPCOMIPCD %{buildroot}%{_libdir}/virtualbox/VBoxXPCOMIPCD
install -p built/bin/vboxshell.py %{buildroot}%{_libdir}/virtualbox/vboxshell.py

cp -a built/bin/components %{buildroot}%{_libdir}/virtualbox/components
cp -a built/bin/*.so %{buildroot}%{_libdir}/virtualbox/

#Install the python bindings
(export VBOX_INSTALL_PATH=%{_libdir}/virtualbox && \
  cd built/bin/sdk/installer && \
  %{__python} ./vboxapisetup.py install --prefix %{_prefix} --root %{buildroot})

# Should the SDK/Bindings be a separate package?
rm -rf built/bin/sdk/installer
cp -a built/bin/sdk %{buildroot}%{_libdir}/virtualbox/sdk

# Host kmod sources
cp -a built/bin/src/* %{buildroot}%{_usrsrc}/virtualbox-kmod-%{version}/

# The VBox binary and a couple of scripts
install -p built/bin/VBox.sh %{buildroot}%{_bindir}/VBox
install -p built/bin/VBoxSysInfo.sh %{buildroot}%{_datarootdir}/virtualbox/VBoxSysInfo.sh
install -p built/bin/VBoxCreateUSBNode.sh %{buildroot}%{_datarootdir}/virtualbox/VBoxCreateUSBNode.sh

install -p -m 4511 built/bin/VirtualBox %{buildroot}%{_libdir}/virtualbox/
install -p -m 4511 built/bin/VBoxHeadless %{buildroot}%{_libdir}/virtualbox/
install -p -m 4511 built/bin/VBoxSVC    %{buildroot}%{_libdir}/virtualbox/
install -p -m 4511 built/bin/VBoxNetDHCP %{buildroot}%{_libdir}/virtualbox/
install -p -m 4511 built/bin/VBoxNetNAT  %{buildroot}%{_libdir}/virtualbox/
install -p -m 4511 built/bin/VBoxNetAdpCtl %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxVolInfo %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxManage         %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxDTrace %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxExtPackHelperApp %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxBalloonCtrl %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxAutostart %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/VBoxTunctl %{buildroot}%{_libdir}/virtualbox/
install -p built/bin/vbox-img %{buildroot}%{_libdir}/virtualbox/

# Most commands are just linked to /usr/bin/VBox
ln -s VBox %{buildroot}%{_bindir}/VirtualBox
ln -s VBox %{buildroot}%{_bindir}/virtualbox
ln -s VBox %{buildroot}%{_bindir}/VBoxManage
ln -s VBox %{buildroot}%{_bindir}/vboxmanage
ln -s VBox %{buildroot}%{_bindir}/VBoxSDL
ln -s VBox %{buildroot}%{_bindir}/vboxsdl
ln -s VBox %{buildroot}%{_bindir}/VBoxHeadless
ln -s VBox %{buildroot}%{_bindir}/vboxheadless
ln -s VBox %{buildroot}%{_bindir}/VBoxBalloonCtrl
ln -s VBox %{buildroot}%{_bindir}/vboxballoonctrl
ln -s VBox %{buildroot}%{_bindir}/VBoxAutostart
ln -s VBox %{buildroot}%{_bindir}/vboxautostart
ln -s %{_libdir}/virtualbox/vbox-img %{buildroot}/%{_bindir}/vbox-img

install -p built/bin/VBox.png %{buildroot}%{_datadir}/pixmaps/VBox.png


# Additions

# Additions kmod-sources
cp -a built/bin/additions/src/* %{buildroot}%{_usrsrc}/virtualbox-guest-kmod-%{version}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/virtualbox/
%{_datarootdir}/virtualbox/
%{_bindir}/VBox
%{_bindir}/VBoxAutostart
%{_bindir}/VBoxBalloonCtrl
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VirtualBox
%{_bindir}/vbox-img
%{_bindir}/vboxautostart
%{_bindir}/vboxballoonctrl
%{_bindir}/vboxheadless
%{_bindir}/vboxmanage
%{_bindir}/vboxsdl
%{_bindir}/virtualbox
%{_datadir}/pixmaps/VBox.png

# kmod
%files devel
%{_libdir}/virtualbox/sdk/
%{_usrsrc}/virtualbox-kmod-%{version}/

%files guest-devel
%{_usrsrc}/virtualbox-guest-kmod-%{version}/

%files -n python-vboxapi
%{python_sitelib}/vboxapi/
%{python_sitelib}/*.egg-info

%changelog

