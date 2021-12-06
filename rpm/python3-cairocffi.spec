# Adapted from Fedora, checks removed

%global srcname cairocffi
%global _version 1.3.0
%bcond_with check

Name:           python-cairocffi
Version:        1.3.0
Release:        1
Summary:        cffi-based cairo bindings for Python
License:        BSD
URL:            https://pypi.python.org/pypi/cairocffi/
Source0:        %{name}-%{version}.tar.bz2
#Patch0:         python-cairocffi-disable-flake8-isort-for-pytest.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi >= 1.1.0
%if %{with check}
# required to run the test suite
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-runner
BuildRequires:  python3-numpy
%endif
BuildRequires:  cairo-devel

BuildRequires:  gdk-pixbuf
BuildRequires:  gdk-pixbuf-modules

%global _description\
cairocffi is a CFFI-based drop-in replacement for Pycairo, a set of\
Python bindings and object-oriented API for cairo.  Cairo is a 2D\
vector graphics library with support for multiple backends including\
image buffers, PNG, PostScript, PDF, and SVG file output.

%description %_description

%package -n python3-cairocffi
Summary:        cffi-based cairo bindings for Python
Requires:       python3-cffi
Requires:       cairo
# required by cairocffi.pixbuf
# Provide the cairocffi[xcb] extras, because there is no reasonable split
# Be aware that %%version is not converted to the Pythonistic version here!
Provides:       python%{python3_pkgversion}dist(cairocffi[xcb]) = %{version}
Provides:       python%{python3_version}dist(cairocffi[xcb]) = %{version}
%{?python_provide:%python_provide python3-cairocffi}

%description -n python3-cairocffi %_description

%prep
%autosetup -n %{name}-%{version}/upstream -p1
# skip pytest
sed -e 's/pytest-runner//' -i setup.cfg

%build
%py3_build

%install
%py3_install

%check
%if %{with check}
# test_xcb.py needs a display
xvfb-run %{__python3} setup.py test
%endif

%files -n python3-cairocffi
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{_version}-py%{python3_version}.egg-info/
