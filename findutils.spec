Summary:	GNU Find Utilities (find, xargs)
Summary(de):	GNU-Suchprogramme (find, xargs)
Summary(fr):	Utilitaires de recherche de GNU (find, xargs)
Summary(pl):	GNU narz�dzia do odnajdywania plik�w (find, xargs)
Summary(tr):	GNU dosya arama ara�lar�
Name:		findutils
Version:	4.1
Release:	33
License:	GPL
Group:		Utilities/File
Group(pl):	Narz�dzia/Pliki
Source0:	ftp://prep.ai.mit.edu/pub/gnu/findutils/%{name}-%{version}.tar.gz
Patch0:		findutils-info.patch
Patch1:		findutils-basename.patch
Patch2:		findutils-glibc.patch
patch3:		findutils-glibc21.patch
Patch4:		findutils-xargsoverflow.patch
Patch5:		findutils-pl_manpages.patch
Patch6:		findutils-mktemp.patch
Patch7:		findutils-numblks.patch
Patch8:		findutils-getshort.patch
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The findutils package contains programs which will help you locate
files on your system. The find utility searches through a hierarchy of
directories looking for files which match a certain set of criteria
(such as a filename pattern). The locate utility searches a database
(create by updatedb) to quickly find a file matching a given pattern.
The xargs utility builds and executes command lines from standard
input arguments (usually lists of file names generated by the find
command).

%description -l de
Das findutils-Paket enth�lt Programme, die dabei helfen, Dateien auf
Ihrem System zu finden. Das Find-Utility durchsucht die
Verzeichnishierarchie nach Dateien, die zu bestimmten Kriterien (z.B.
Dateiname) passen. Das locate-Utility durchsucht eine Datenbank
(erzeugt durch updatedb), um die Dateien schneller finden zu k�nnen.
xargs konstruiert Kommandozeilen von der Standardeingabe (z.B.
Dateilisten, die von find erzeugt werden), und f�hrt sie aus.

%description -l fr
Ce package contient des programmes pour vous aider � localiser des
fichiers sur votre syst�me. Le programme find peut rechercher �
travers une hi�rarchie de r�pertoires des fichiers conformes �
certains crit�res (comme un type de nom).

%description -l pl
W pakiecie znajduj� si� narz�dzia pozwalaj�ce na poszukiwanie
okre�lonych plik�w. Program find s�u�y do poszukiwania w drzewie
katalog�w plik�w o okre�lonych parametrach, jak nazwa, uprawnienia,
typ czy data ostatniej modyfikacji.

%description -l tr
Bu pakette yer alan yaz�l�mlar sisteminizde yer alan dosyalar�
bulabilmeniz i�in haz�rlanm��lard�r. find program� ile belirli
�zellikleri olan bir yaz�l�m� bir dizin hiyerar�isi alt�nda
arayabilirsiniz.

%prep
%setup  -q
%patch0 -p1 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
autoconf
LDFLAGS="-s"; export LDFLAGS
%configure 

make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/pl/man1

make install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}
	
install pl/*.1  $RPM_BUILD_ROOT%{_mandir}/pl/man1

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/find.info* \
	$RPM_BUILD_ROOT%{_mandir}/{man?/*,pl/man1/*} \
	NEWS README TODO ChangeLog

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {NEWS,README,TODO,ChangeLog}.gz
%attr(755,root,root) %{_bindir}/find
%attr(755,root,root) %{_bindir}/xargs

%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*
%lang(pl) %{_mandir}/pl/man1/*
%{_infodir}/find.info*
