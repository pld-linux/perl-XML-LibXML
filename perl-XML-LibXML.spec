#
# Conditional build:
# _with_tests - perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	LibXML
Summary:	XML::LibXML Perl module
Summary(cs):	Modul XML::LibXML pro Perl
Summary(da):	Perlmodul XML::LibXML
Summary(de):	XML::LibXML Perl Modul
Summary(es):	Módulo de Perl XML::LibXML
Summary(fr):	Module Perl XML::LibXML
Summary(it):	Modulo di Perl XML::LibXML
Summary(ja):	XML::LibXML Perl ¥â¥¸¥å¡¼¥ë
Summary(ko):	XML::LibXML ÆÞ ¸ðÁÙ
Summary(no):	Perlmodul XML::LibXML
Summary(pl):	Modu³ Perla XML::LibXML
Summary(pt):	Módulo de Perl XML::LibXML
Summary(pt_BR):	Módulo Perl XML::LibXML
Summary(ru):	íÏÄÕÌØ ÄÌÑ Perl XML::LibXML
Summary(sv):	XML::LibXML Perlmodul
Summary(uk):	íÏÄÕÌØ ÄÌÑ Perl XML::LibXML
Summary(zh_CN):	XML::LibXML Perl Ä£¿é
Name:		perl-%{pdir}-%{pnam}
%define		_ver	1.54_3
Version:	%(echo %{_ver} | sed 's:_:\.:')
Release:	2
License:	GPL
Group:		Development/Languages/Perl
#Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
Source0:	http://www.cpan.org/authors/id/P/PH/PHISH/%{pdir}-%{pnam}-%{_ver}.tar.gz
Patch0:		%{name}-Makefile.patch
BuildRequires:	libxml2-devel >= 2.4.8
BuildRequires:	perl-XML-LibXML-Common
BuildRequires:	perl-XML-NamespaceSupport >= 1.07
BuildRequires:	perl-XML-SAX >= 0.11
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	rpm-perlprov >= 4.0.2-104
Requires:	libxml2 >= 2.4.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements much of the DOM Level 2 API as an interface to
the Gnome libxml2 library. This makes it a fast and highly capable
validating XML parser library, as well as a high performance DOM.

%description -l pl
Ten modu³ to implementacja wiêkszo¶ci API DOM Level 2 jako interfejsu
do biblioteki Gnome libxml2. Daje to szybki i o du¿ych mo¿liwo¶ciach
parser sprawdzaj±cy poprawno¶æ XML, a tak¿e wysoko wydajny DOM.

%package SAX
Summary:	XML::LibXML::SAX perl module
Summary(pl):	Modu³ perla XML::LibXML::SAX
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}
Requires(post,preun):	perl-XML-LibXML-SAX

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
%setup -q -n %{pdir}-%{pnam}-%{_ver}
%patch0 -p1

%build
%{__perl} Makefile.PL
%{__make} OPTIMIZE="%{rpmcflags}"

# dtd test fails for unknown reason
%{?_with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install example/{*.pl,*.xml,*.dtd,*.xhtml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex
install example/complex/{*.xml,*.dtd} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd
install example/complex/dtd/*.dtd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd

%clean
rm -rf $RPM_BUILD_ROOT

%post SAX
umask 022
perl -MXML::SAX -e "XML::SAX->add_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%preun SAX
umask 022
perl -MXML::SAX -e "XML::SAX->remove_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_sitearch}/XML/LibXML.pm
%{perl_sitearch}/XML/LibXML/[^S]*.pm
%{perl_sitearch}/auto/XML/LibXML/LibXML.bs
%attr(755,root,root) %{perl_sitearch}/auto/XML/LibXML/LibXML.so
%{_mandir}/man3/XML::LibXML.3pm*
%{_mandir}/man3/XML::LibXML::[^S]*
%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/x*.pl
%{_examplesdir}/%{name}-%{version}/[^x]*

%files SAX
%defattr(644,root,root,755)
%dir %{perl_sitearch}/XML/LibXML/SAX
%{perl_sitearch}/XML/LibXML/SAX.pm
%{perl_sitearch}/XML/LibXML/SAX/*.pm
%{_mandir}/man3/XML::LibXML::SAX.3pm*
%{_mandir}/man3/XML::LibXML::SAX::*
