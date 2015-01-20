# gnash-rpm
GNU gnash RPM spec file and notes

Gnash can replace Adobe's flash-plugin package on Fedora and RHEL.  At least in
most circumstances.  It does not work with all Flash content, but neither does
Adobe's plugin.  Adobe has discontinued development of the Linux plugin and is
only releasing security updates.  I have found Gnash usable with YouTube, which
is a huge step for open source SWF players.

The project contains my notes and spec file to build Gnash as an RPM you can
install on Fedora or RHEL systems.  Please see the spec file for information
about the BuildRequires.
