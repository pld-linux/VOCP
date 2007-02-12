
# TODO:
# -move vocpweb.cgi to cgi-bin directory or adding
#   <Directory %{_vocpwebdir}>
#       Options ExecCGI
#   </Directory>
#   to httpd.conf, what with diff in locaton confs between apatche 1.x and 2.x ?,
# -make to work pass checking in xvocp.pl, luzik is to lame in perl,
# -add .desktop files and icons, min. for callcenter & boxconf,
# -full test package,
# -translate description,
# -play with secure stuff, attr for examle, luzik is to lame in sec,
# -fix BR, for each package
# -try runing on perl-5.6.1

%include	/usr/lib/rpm/macros.perl

%define		_vocpwebdir	/home/services/httpd/html/vocp

Summary:	VOCP is a complete messaging solution for voice modems
Summary(pl.UTF-8):	VOCP to pełna obsługa wiadomości dla modemów głosowych
Name:		VOCP
Version:	0.9.3
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/vocp/%{name}-%{version}.tar.bz2
# Source0-md5:	1a570a1f5af11786b39f6aed4304b5c3
Source1:	%{name}.logrotate
Patch0:		%{name}-vars.patch
Patch1:		%{name}-bin.patch
Patch2:		%{name}-vocpweb.patch
Patch3:		%{name}-doc.patch
URL:		http://www.vocpsystem.com/
Requires:	festival
Requires:	lame
Requires:	logrotate
Requires:	perl-Modem-Vgetty
Requires:	vorbis-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Much more than an answering machine, VOCP transforms your computer
into a full-featured call answering and voice messaging system.

%description -l pl.UTF-8
VOCP to dużo więcej niż automatyczna sekretarka - zamienia komputer na
w pełni funkcjonalny system odpowiedzi i komunikatów głosowych.

%package perl-modules
Summary:	Perl modules for VOCP
Summary(pl.UTF-8):	Moduły Perla dla VOCP
Group:		Applications/Communications
Requires:	perl >= 5.8.0

%description perl-modules
Perl modules for VOCP.

%description perl-modules -l pl.UTF-8
Moduły Perla dla VOCP.

%package vocpweb
Summary:	Web GUI for VOCP
Summary(pl.UTF-8):	Interfejs graficzny WWW dla VOCP
Group:		Applications/Communications
Requires:	%{name}-perl-modules

%description vocpweb
Web GUI for VOCP.

%description vocpweb -l pl.UTF-8
Interfejs graficzny WWW dla VOCP.

%prep
%setup -q -n vocp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd prog/bin
%{__cc} %{rpmcflags} %{rpmldflags} -o pwcheck pwcheck.c
%{__cc} %{rpmcflags} %{rpmldflags} -o xfer_to_vocp xfer_to_vocp.c

cd ../VOCP
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/vocp \
	$RPM_BUILD_ROOT%{_datadir}/vocp/{images,messages,run,sounds,lib} \
	$RPM_BUILD_ROOT%{_var}/spool/voice/{commands,incoming/cache,messages} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_vocpwebdir}/{img,sounds,tpl} \
	$RPM_BUILD_ROOT/etc/logrotate.d \
	$RPM_BUILD_ROOT/var/log

%{__make} install -C prog/VOCP \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%%{perl_vendorlib}/auto
cp -R images $RPM_BUILD_ROOT%{_datadir}/vocp
cp -R sounds $RPM_BUILD_ROOT%{_datadir}/vocp
cp -R messages $RPM_BUILD_ROOT%{_datadir}/vocp
cp -R prog/lib $RPM_BUILD_ROOT%{_datadir}/vocp
cp prog/bin/README prog/bin/README-bin
cp -R commands $RPM_BUILD_ROOT%{_var}/spool/voice
cp -R messages/*.rmd $RPM_BUILD_ROOT%{_var}/spool/voice/messages
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install vocpweb/*.html $RPM_BUILD_ROOT%{_vocpwebdir}
install vocpweb/styles.css $RPM_BUILD_ROOT%{_vocpwebdir}
install vocpweb/img/*.gif $RPM_BUILD_ROOT%{_vocpwebdir}/img
install vocpweb/sounds/*.html $RPM_BUILD_ROOT%{_vocpwebdir}/sounds
install vocpweb/tpl/*.html $RPM_BUILD_ROOT%{_vocpwebdir}/tpl
install vocpweb/vocpweb.cgi $RPM_BUILD_ROOT%{_vocpwebdir}
touch $RPM_BUILD_ROOT/var/log/{vocp-calls.log,vocp.log,voicelog}
for i in boxconf.pl convert_boxconf.pl pvftomp3 pwcheck \
toggleEmail2Vm.pl vocphax.pl xfer_to_vocp xvocp.pl \
callcenter.pl convert_fax.sh email2vm.pl pvftoogg \
pwcheck.pl txttopvf vocplocal.pl xfer_to_vocp \
cnd-logger.pl cryptpass.pl messages.pl pwcheck \
view_fax.sh wav2rmd.pl xfer_to_vocp.pl ../vocp.pl; do
	install prog/bin/$i $RPM_BUILD_ROOT%{_bindir}
done
for i in boxes.conf boxes.conf.sample boxes.conf.shadow cid-filter.conf vocp.conf; do
	install prog/$i $RPM_BUILD_ROOT%{_sysconfdir}/vocp
done

install prog/lib/XVOCP.pm $RPM_BUILD_ROOT%{perl_vendorlib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL CHANGELOG prog/bin/README-bin doc/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vocp/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/vocp
%attr(1777,root,root) %dir /var/spool/voice/incoming/cache
%attr(755,root,root) /var/spool/voice/commands/*
%{_var}/spool/voice/messages/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) /var/log/*log

%files perl-modules
%defattr(644,root,root,755)
%{perl_vendorlib}/VOCP.pm
%{perl_vendorlib}/XVOCP.pm
%{perl_vendorlib}/VOCP
%{perl_vendorlib}/auto/VOCP/autosplit.ix
%{_mandir}/man3/*

%files vocpweb
%defattr(644,root,root,755)
%doc vocpweb/INSTALL vocpweb/README vocpweb/SECURITY
%dir %{_vocpwebdir}
%attr(1777,root,root) %dir %{_vocpwebdir}/sounds
%{_vocpwebdir}/index.html
%{_vocpwebdir}/styles.css
%{_vocpwebdir}/vocpwebhelp.html
%{_vocpwebdir}/img/*.gif
%{_vocpwebdir}/sounds/index.html
%{_vocpwebdir}/tpl/*.html
%attr(4755,root,root) %{_vocpwebdir}/vocpweb.cgi
