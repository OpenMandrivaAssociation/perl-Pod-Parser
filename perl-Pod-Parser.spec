Name:           perl-Pod-Parser
Version:        1.61
Release:        3%{?dist}
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
License:        GPL+ or Artistic

URL:            http://search.cpan.org/dist/Pod-Parser/
Source0:        http://www.cpan.org/authors/id/M/MA/MAREKR/Pod-Parser-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-devel
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.82
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
# Symbol not used with recent perl
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Test::More) >= 0.6
# Circular dependency Pod::Checker <-> Pod::Parser
BuildRequires:  perl(Pod::Checker) >= 1.40
Requires:       perl(Config)
# Circular dependency Pod::Usage <-> Pod::Select

%description
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.

%prep
%setup -q -n Pod-Parser-%{version}
find -type f -exec chmod -x {} +
chmod +x scripts/*
for F in ANNOUNCE CHANGES README TODO; do
    tr -d '\r' < "$F" > "${F}.unix"
    touch -r "$F" "${F}.unix"
    mv "${F}.unix" "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
chmod -Rf a+rX,u+w,g-w,o-w $RPM_BUILD_ROOT/*
# conflicts with perl
rm $RPM_BUILD_ROOT%{_mandir}/man1/podselect.*

%check
make test

%files
%doc ANNOUNCE CHANGES README TODO
%{_bindir}/podselect
%{perl_vendorlib}/*
#${_mandir}/man1/*
%{_mandir}/man3/*
