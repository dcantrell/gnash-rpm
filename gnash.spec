%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:    gnash
Version: 0.8.10
Release: 1%{?dist}
Summary: GNU SWF player

Group:   Applications/Multimedia
License: GPLv3+
URL:     https://www.gnu.org/software/gnash/
Source0: ftp://ftp.gnu.org/pub/gnu/%{name}/%{version}/%{name}-%{version}.tar.bz2

Patch0:  gnash-0.8.10-CVE-2012-1175-1.patch
Patch1:  gnash-0.8.10-build.patch

Requires(post):  info
Requires(preun): info

# These packages come from the main Fedora or RHEL (or CentOS...) repos:
BuildRequires: pygtk2-devel
BuildRequires: SDL-devel
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: giflib-devel
BuildRequires: libjpeg-devel
BuildRequires: texinfo-tex
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: speex-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: xulrunner-devel
BuildRequires: boost-devel
BuildRequires: agg-devel
BuildRequires: doxygen
BuildRequires: fop
BuildRequires: texlive-xmltex-bin
BuildRequires: desktop-file-utils

# These packages are in EPEL for RHEL or the main Fedora repo for Fedora:
BuildRequires: docbook2X
BuildRequires: libssh-devel

# XXX:
# Not done yet.  There are a lot of things required to run the test suite that
# are not available as packages.  I may end up packaging up the required things,
# but not right now.  Required projects:
#
#     libming and Ming utilities (http://www.libming.org/)
#     MTASC compiler (http://mtasc.org)
#     HAXE compiler (http://haxe.org)
#     swfmill (http://swfmill.org)
#     csound (http://www.csounds.com)
#
## These packages are only necessary for %check.  If you want to build locally,
## you might not want all of these.  In which case just comment out these lines
## and comment out the %check block.
##
## In the main RHEL and Fedora repos:
#BuildRequires: dejagnu
## In rpmfusion-free repos:
#BuildRequires: swftools
## Built locally from SRPMs:

# *****************
# * THE BEST PART *
# *****************
Conflicts: flash-plugin

%description
Gnash is a player for animated "movies" in the Macromedia Shockwave Flash
(SWF) format.  It can be run as a graphical application, as a Web browser
plugin, or as a library used by other programs.  It is not yet complete;
it does not correctly handle every SWF file.

%package devel
Summary:  Gnash development libraries and headers
Group:    Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Development libraries and header files for GNU Gnash.

%prep
%setup -q
%patch0 -p1 -b .CVE-2012-1175
%patch1 -p1 -b .build

%build
# Just configure for building a Firefox-compatible plugin.  If you are
# interested in a plugin for other browsers, patches welcome.
%configure --enable-gui=gtk \
           --enable-sound=sdl \
           --enable-media=gst \
           --enable-device=egl,x11 \
           --disable-static \
           --enable-python \
           --enable-offscreen \
           --enable-ssh \
           --enable-ssl \
           --disable-kparts3 \
           --disable-kparts4 \
           --enable-npapi \
           --enable-plugins \
           --enable-ghelp \
           --enable-docbook \
           --enable-visibility \
           --with-plugins-install=system \
           --with-npapi-install=system \
           --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
           --without-gconf
make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
make install-plugin DESTDIR=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/%{name}/libgnashdevice.la
rm -f %{buildroot}%{_mandir}/man1/cygnal.1*

# not built
rm -f %{buildroot}%{_mandir}/man1/flvdumper.1*
rm -f %{buildroot}%{_mandir}/man1/soldumper.1*

# handled by the %doc macro in %files
rm -rf %{buildroot}%{_docdir}

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/gnash_ref.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gnash_user.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gnash_ref.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gnash_user.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README README.git TODO
%doc doc/C/gnashref.html doc/C/gnashuser.html doc/C/images/rtmp.png
%config(noreplace) %{_sysconfdir}/gnashpluginrc
%config(noreplace) %{_sysconfdir}/gnashrc
%{_bindir}/eglinfo
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%{_bindir}/gnash-gtk-launcher
%{_bindir}/gnash
%{_bindir}/gtk-gnash
%{_bindir}/rtmpget
%{_libdir}/%{name}/libgnashbase-%{version}.so
%{_libdir}/%{name}/libgnashcore-%{version}.so
%{_libdir}/%{name}/libgnashdevice-%{version}.so
%{_libdir}/%{name}/libgnashmedia-%{version}.so
%{_libdir}/%{name}/libgnashrender-%{version}.so
%{_libdir}/%{name}/libgnashsound-%{version}.so
%{_libdir}/mozilla/plugins/libgnashplugin.so
%{python2_sitearch}/gtk-2.0/%{name}.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm
%{_datadir}/%{name}/GnashG.png
%{_datadir}/%{name}/gnash-splash.swf
%{_datadir}/%{name}/gnash_128_96.ico
%{_infodir}/gnash_ref.info.gz
%{_infodir}/gnash_user.info.gz
%{_mandir}/man1/findmicrophones.1.gz
%{_mandir}/man1/findwebcams.1.gz
%{_mandir}/man1/gnash-gtk-launcher.1.gz
%{_mandir}/man1/gnash.1.gz
%{_mandir}/man1/gtk-gnash.1.gz
%{_mandir}/man1/rtmpget.1.gz

%files devel
%defattr(-,root,root)
%{_bindir}/gprocessor
%{_includedir}/%{name}
%{_libdir}/%{name}/libgnashbase.so
%{_libdir}/%{name}/libgnashcore.so
%{_libdir}/%{name}/libgnashdevice.so
%{_libdir}/%{name}/libgnashmedia.so
%{_libdir}/%{name}/libgnashrender.so
%{_libdir}/%{name}/libgnashsound.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man1/gprocessor.1.gz

%changelog
* Mon Jan 19 2015 David Cantrell <dcantrell@redhat.com> - 0.8.10-1
- Initial package
