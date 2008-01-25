#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
#
Summary:	GNU Find Utilities (find, xargs)
Summary(de.UTF-8):	GNU-Suchprogramme (find, xargs)
Summary(es.UTF-8):	Utilitarios de búsqueda de la GNU
Summary(fr.UTF-8):	Utilitaires de recherche de GNU (find, xargs)
Summary(pl.UTF-8):	Narzędzia GNU do odnajdywania plików (find, xargs)
Summary(pt_BR.UTF-8):	Utilitários de procura da GNU
Summary(tr.UTF-8):	GNU dosya arama araçları
Name:		findutils
Version:	4.2.32
Release:	1
Epoch:		1
License:	GPL v3+
Group:		Applications/File
# development versions at ftp://alpha.gnu.org/gnu/findutils/
Source0:	ftp://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz
# Source0-md5:	aaa6beeb41a6f04963dff58f24a55b96
#Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
Source1:	%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	e76388b0c3218eec3557d05ccd6d6515
Patch0:		%{name}-info.patch
Patch1:		%{name}-selinux.patch
Patch2:		%{name}-man-selinux.patch
Patch3:		%{name}-pl.po-update.patch
URL:		http://www.gnu.org/software/findutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.14.5
%{?with_selinux:BuildRequires:	libselinux-devel}
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

%description -l de.UTF-8
Das findutils-Paket enthält Programme, die dabei helfen, Dateien auf
Ihrem System zu finden. Das Find-Utility durchsucht die
Verzeichnishierarchie nach Dateien, die zu bestimmten Kriterien (z.B.
Dateiname) passen. Das locate-Utility durchsucht eine Datenbank
(erzeugt durch updatedb), um die Dateien schneller finden zu können.
xargs konstruiert Kommandozeilen von der Standardeingabe (z.B.
Dateilisten, die von find erzeugt werden), und führt sie aus.

%description -l es.UTF-8
Este paquete contiene programas para ayúdalo a localizar archivos en
tu sistema. El programa find puede pesquisar, a través de una
jerarquía de directorios, buscando por archivos que obedezcan a un
cierto conjunto de criterios (como nombre de archivo modelo).

%description -l fr.UTF-8
Ce package contient des programmes pour vous aider à localiser des
fichiers sur votre système. Le programme find peut rechercher à
travers une hiérarchie de répertoires des fichiers conformes à
certains critères (comme un type de nom).

%description -l pl.UTF-8
W pakiecie znajdują się narzędzia pozwalające na poszukiwanie
określonych plików. Program find służy do poszukiwania w drzewie
katalogów plików o określonych parametrach, jak nazwa, uprawnienia,
typ czy data ostatniej modyfikacji.

%description -l pt_BR.UTF-8
Esse pacote contém programas para ajudá-lo a localizar arquivos em seu
sistema. O programa find pode procurar através de uma hierarquia de
diretórios procurando por arquivos que obedeçam um certo conjunto de
critérios (como nome de arquivo modelo).

%description -l tr.UTF-8
Bu pakette yer alan yazılımlar sisteminizde yer alan dosyaları
bulabilmeniz için hazırlanmışlardır. find programı ile belirli
özellikleri olan bir yazılımı bir dizin hiyerarşisi altında
arayabilirsiniz.

%prep
%setup -q
%patch3 -p1
%patch0 -p1
%{?with_selinux:%patch1 -p1}
# patch2 is applied in install stage

rm -f po/stamp-po

%build
%{__aclocal} -I gnulib/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{?with_selinux:patch -p0 -d $RPM_BUILD_ROOT%{_mandir} < %{PATCH2}}

# xargs is wanted in /bin
install -d $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%{_bindir}/xargs $RPM_BUILD_ROOT/bin

# unpackaged locate
rm -f $RPM_BUILD_ROOT%{_bindir}/{locate,updatedb} \
	$RPM_BUILD_ROOT%{_libdir}/{bigram,code,frcode} \
	$RPM_BUILD_ROOT%{_mandir}/{,*/}man?/{locate.1,updatedb.1,locatedb.5}*

rm -f $RPM_BUILD_ROOT{%{_infodir}/dir,%{_mandir}/README.findutils-non-english-man-pages}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/find
%attr(755,root,root) /bin/xargs

%{_mandir}/man1/[fx]*
%lang(de) %{_mandir}/de/man1/[fx]*
%lang(es) %{_mandir}/es/man1/[fx]*
%lang(fi) %{_mandir}/fi/man1/[fx]*
%lang(fr) %{_mandir}/fr/man1/[fx]*
%lang(hu) %{_mandir}/hu/man1/[fx]*
%lang(it) %{_mandir}/it/man1/[fx]*
%lang(ja) %{_mandir}/ja/man1/[fx]*
%lang(nl) %{_mandir}/nl/man1/[fx]*
%lang(pl) %{_mandir}/pl/man1/[fx]*
%lang(zh_CN) %{_mandir}/zh_CN/man1/[fx]*
%{_infodir}/find.info*
