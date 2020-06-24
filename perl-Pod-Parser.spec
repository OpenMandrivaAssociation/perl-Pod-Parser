%define modname Pod-Parser
%define modver 1.63


Summary:	Basic perl modules for handling Plain Old Documentation (POD)
Name:		perl-%{modname}
Version:	%{perl_convert_version %{modver}}
Release:	1
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Pod-Parser
Source0:	https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)

%description
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.

%prep
%autosetup -n Pod-Parser-%{version} -p1

find -type f -exec chmod -x {} +
chmod +x scripts/*
for F in ANNOUNCE CHANGES README TODO; do
    tr -d '\r' < "$F" > "${F}.unix"
    touch -r "$F" "${F}.unix"
    mv "${F}.unix" "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install

%check
make test

%files
%doc ANNOUNCE CHANGES README TODO
%{_bindir}/podselect
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
