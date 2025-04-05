#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Manipulate and inspect Sphinx objects.inv files
Summary(pl.UTF-8):	Operacje i badanie plików object.inv Sphinksa
Name:		python3-sphobjinv
Version:	2.3.1.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphobjinv/
Source0:	https://files.pythonhosted.org/packages/source/s/sphobjinv/sphobjinv-%{version}.tar.gz
# Source0-md5:	069226ea6bb15ed387360303961919fb
Patch0:		no-latin1-test.patch
URL:		https://pypi.org/project/sphobjinv/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.6
BuildRequires:	python3-attrs >= 19.2
BuildRequires:	python3-certifi
BuildRequires:	python3-dictdiffer >= 0.9.0
BuildRequires:	python3-jsonschema >= 3.0
BuildRequires:	python3-pytest >= 4.4.0
BuildRequires:	python3-pytest-check >= 1.1.2
BuildRequires:	python3-stdio_mgr
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_issues
BuildRequires:	python3-sphinx_removed_in
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-programoutput
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Manipulate and inspect Sphinx objects.inv files.

%description -l pl.UTF-8
Operacje i badanie plików object.inv Sphinksa.

%package apidocs
Summary:	API documentation for Python sphobjinv module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphobjinv
Group:		Documentation

%description apidocs
API documentation for Python sphobjinv module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphobjinv.

%prep
%setup -q -n sphobjinv-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_check.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_cli_invocations'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md LICENSE.txt README.md
%attr(755,root,root) %{_bindir}/sphobjinv
%{py3_sitescriptdir}/sphobjinv
%{py3_sitescriptdir}/sphobjinv-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_static,api,cli,*.html,*.js}
%endif
