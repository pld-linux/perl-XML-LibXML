%include	/usr/lib/rpm/macros.perl

%define	pdir	XML
%define	pnam	LibXML

Summary:	XML-LibXML perl module
Summary(pl):	Modu³ perla XML-LibXML
Name:		perl-%{pdir}-%{pnam}
Version:	1.40
Release:	1
License:	GPL
Group:		Development/Languages/Perl
Source0:	ftp://ftp.cpan.org/pub/CPAN/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
Patch0:		%{name}-Makefile.patch
BuildRequires:	rpm-perlprov >= 4.0.2-56
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	perl-XML-SAX
BuildRequires:	libxml2-devel >= 2.4.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	libxml2 >= 2.4.8

%description
This module implements much of the DOM Level 2 API as an interface to
the Gnome libxml2 library. This makes it a fast and highly capable
validating XML parser library, as well as a high performance DOM.

%description -l pl
Ten modu³ to implementacja wiêkszo¶ci API DOM Level 2 jako interfejsu
do biblioteki Gnome libxml2. Daje to szybki i o du¿ych mo¿liwo¶ciach
parser sprawdzaj±cy poprawno¶æ XML, a tak¿e wysoko wydajny DOM.

%package SAX
Summary:	XML-LibXML-SAX perl module
Summary(pl):	Modu³ perla XML-LibXML-SAX
Group:		Development/Languages/Perl

%description SAX
This class allows you to generate SAX2 events using LibXML. Note that
this is not a stream based parser, instead it parses documents into a
DOM and traverses the DOM tree. The reason being that libxml2's stream
based parsing is extremely primitive, and would require an extreme
amount of work to allow SAX2 parsing in a stream manner.

%description SAX -l pl
Ta klasa pozwala generowaæ zdarzenia SAX2 przy u¿yciu LibXML2. To nie
jest parser bazuj±cy na strumieniach - przetwarza dokumenty na DOM i
nastêpnie wêdruje po drzewie DOM. Wynika to z faktu, ¿e w libxml2
parsowanie oparte na strumieniach jest bardzo prymitywne i wymaga³oby
wiele pracy, aby umo¿liwiæ strumieniowe parsowanie SAX2.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
perl Makefile.PL
%{__make} OPTIMIZE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install example/{*.pl,*.xml,*.dtd,*.xhtml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex
install example/complex/{*.xml,*.dtd} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd
install example/complex/dtd/*.dtd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd

gzip -9nf Changes README PHISHS.CHANGES

%post SAX
perl -MXML::SAX -e "XML::SAX->add_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%preun SAX
perl -MXML::SAX -e "XML::SAX->remove_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%{perl_sitearch}/XML/LibXML.pm
%dir %{perl_sitearch}/XML/LibXML
%{perl_sitearch}/XML/LibXML/*.pm
%{perl_sitearch}/XML/LibXML/*.pod
%dir %{perl_sitearch}/auto/XML/LibXML
%{perl_sitearch}/auto/XML/LibXML/LibXML.bs
%attr(755,root,root) %{perl_sitearch}/auto/XML/LibXML/LibXML.so
%{_mandir}/man3/XML::LibXML.3pm.gz
%{_mandir}/man3/XML::LibXML::[^S][^A][^X]*
%{_examplesdir}/%{name}-%{version}

%files SAX
%defattr(644,root,root,755)
%dir %{perl_sitearch}/XML/LibXML/SAX
%{perl_sitearch}/XML/LibXML/SAX/*.pm
%{_mandir}/man3/XML::LibXML::SAX::*
