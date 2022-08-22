#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#

# see Makefile.PL /blacklist, choose first OK version to ensure skipping all broken releases
%define	libxml2_ver	1:2.9.6

%define		pdir	XML
%define		pnam	LibXML
Summary:	XML::LibXML - interface to the GNOME libxml2 library
Summary(pl.UTF-8):	XML::LibXML - interfejs do biblioteki libxml2 z GNOME
Name:		perl-XML-LibXML
Version:	2.0207
Release:	4
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/XML/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	d943c3ff20e19c376f08adcbc4158019
URL:		https://metacpan.org/release/XML-LibXML
BuildRequires:	libxml2-devel >= %{libxml2_ver}
BuildRequires:	perl-Alien-Libxml2 >= 0.14
# Alien::Base::Wrapper
BuildRequires:	perl-Alien-Base >= 0.64_01
BuildRequires:	perl-ExtUtils-MakeMaker >= 6.56
BuildRequires:	perl-devel >= 1:5.8.1
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	iconv
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl-Encode
BuildRequires:	perl-Scalar-List-Utils
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-XML-NamespaceSupport >= 1.07
BuildRequires:	perl-XML-SAX >= 0.11
%endif
Requires:	libxml2 >= %{libxml2_ver}
Requires:	perl-XML-NamespaceSupport >= 1.07
Requires:	perl-XML-SAX >= 0.11
Provides:	perl-XML-LibXML-XPathContext = %{version}
Obsoletes:	perl-XML-LibXML-Common < 0.14
Obsoletes:	perl-XML-LibXML-XPathContext <= 0:0.07
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements much of the DOM Level 2 API as an interface to
the GNOME libxml2 library. This makes it a fast and highly capable
validating XML parser library, as well as a high performance DOM.

%description -l pl.UTF-8
Ten moduł to implementacja większości API DOM Level 2 jako interfejsu
do biblioteki GNOME libxml2. Daje to szybki i mający duże możliwości
analizator sprawdzający poprawność XML-a, a także wysoko wydajny DOM.

%package SAX
Summary:	XML::LibXML::SAX Perl module - XML::LibXML direct SAX parser
Summary(pl.UTF-8):	Moduł Perla XML::LibXML::SAX - bezpośredni analizator SAX z XML::LibXML
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description SAX
This class allows you to generate SAX2 events using LibXML. Note that
this is not a stream based parser, instead it parses documents into a
DOM and traverses the DOM tree. The reason being that libxml2's stream
based parsing is extremely primitive, and would require an extreme
amount of work to allow SAX2 parsing in a stream manner.

%description SAX -l pl.UTF-8
Ta klasa pozwala generować zdarzenia SAX2 przy użyciu LibXML2. To nie
jest analizator oparty na strumieniach - przetwarza dokumenty na DOM i
następnie wędruje po drzewie DOM. Wynika to z faktu, że w libxml2
analiza oparta na strumieniach jest bardzo prymitywna i wymagałaby
wiele pracy, aby umożliwić strumieniową analizę SAX2.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
SKIP_SAX_INSTALL=true;
export SKIP_SAX_INSTALL

%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install example/{*.pl,*.xml,*.dtd,*.xhtml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex
install example/complex/{*.xml,*.dtd} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd
install example/complex/dtd/*.dtd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd

# mans are provided
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/XML/{LibXML.pod,LibXML/*.pod,LibXML/SAX/*.pod}

%clean
rm -rf $RPM_BUILD_ROOT

%post SAX
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%preun SAX
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README TODO
%{perl_vendorarch}/XML/LibXML.pm
%dir %{perl_vendorarch}/XML/LibXML
%{perl_vendorarch}/XML/LibXML/[!S]*.pm
%dir %{perl_vendorarch}/auto/XML/LibXML
%attr(755,root,root) %{perl_vendorarch}/auto/XML/LibXML/LibXML.so
%{_mandir}/man3/XML::LibXML.3pm*
%{_mandir}/man3/XML::LibXML::[!S]*
%{_mandir}/man3/XML::LibXML::S[!A]*
%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/x*.pl
%{_examplesdir}/%{name}-%{version}/[!x]*

%files SAX
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/XML/LibXML/SAX
%{perl_vendorarch}/XML/LibXML/SAX.pm
%{perl_vendorarch}/XML/LibXML/SAX/*.pm
%{_mandir}/man3/XML::LibXML::SAX.3pm*
%{_mandir}/man3/XML::LibXML::SAX::*
