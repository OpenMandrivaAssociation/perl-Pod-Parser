# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Pod_Parser_enables_optional_test
%else
%bcond_with perl_Pod_Parser_enables_optional_test
%endif

Name:           perl-Pod-Parser
Version:        1.63
Release:        442%{?dist}
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Pod-Parser
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.82
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
# Getopt::Long not used for tests
# Pod::Usage not used for tests
BuildRequires:  perl(strict)
# Symbol not used since perl 5.6
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.6
# Circular dependency Pod::Checker <-> Pod::Parser
BuildRequires:  perl(Pod::Checker) >= 1.40
# VMS::Filespec not used
%if %{with perl_Pod_Parser_enables_optional_test} && !%{defined perl_bootstrap}
# Optional tests:
BuildRequires:  perl(IO::String)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
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
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc ANNOUNCE CHANGES README TODO
%{_bindir}/podselect
%{perl_vendorlib}/Pod/*
%{_mandir}/man1/*
%{_mandir}/man3/*
