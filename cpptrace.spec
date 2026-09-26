%define major 0
%define libname %mklibname cpptrace %{major}
%define devname %mklibname -d cpptrace

Name:		cpptrace
Version:	1.0.4
Release:	3
Summary:	Simple, portable, and self-contained stacktrace library for C++11 and newer
Group:		Development/C++
License:	MIT
URL:		https://github.com/jeremy-rifkin/%{name}
Source0:	https://github.com/jeremy-rifkin/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(libdwarf)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(libzstd)

%description
Cpptrace is a simple and portable C++ stacktrace library supporting
C++11 and greater on Linux, macOS, and Windows including MinGW and
Cygwin environments. In addition to providing access to stack
traces, cpptrace also provides a mechanism for getting stacktraces
from thrown exceptions, which is valuable for debugging and
triaging.

%package -n %{libname}
Summary:	Shared library for cpptrace

%description -n %{libname}
Shared library for cpptrace, a portable C++ stacktrace library.

%package -n %{devname}
Summary:	Development files for cpptrace
Requires:	%{libname} = %{EVRD}
Requires:	pkgconfig(libdwarf)
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Headers and CMake package config for cpptrace, a portable C++
stacktrace library.

%prep
%autosetup -p1

%build
%cmake \
	-DCPPTRACE_BUILD_TESTING=OFF \
	-DCPPTRACE_DEMANGLE_WITH_CXXABI=ON \
	-DCPPTRACE_FIND_LIBDWARF_WITH_PKGCONFIG=ON \
	-DCPPTRACE_USE_EXTERNAL_ZSTD=ON \
	-DCPPTRACE_USE_EXTERNAL_LIBDWARF=ON \
	-DCPPTRACE_UNWIND_WITH_LIBUNWIND=ON \
	-DBUILD_SHARED_LIBS=ON
%make_build -C build

%install
%make_install -C build
# The exported cmake config calls find_dependency(libdwarf), but libdwarf
# is found via pkg-config here, not a cmake package — nothing on this
# distro provides cmake(libdwarf). Strip it; pkgconfig(libdwarf) above
# already covers the real dependency.
sed -i '/find_dependency(libdwarf/d' %{buildroot}%{_libdir}/cmake/cpptrace/*.cmake

%files -n %{libname}
%license LICENSE
%{_libdir}/libcpptrace.so.*

%files -n %{devname}
%{_libdir}/libcpptrace.so
%{_libdir}/cmake/cpptrace
%{_includedir}/cpptrace
%{_includedir}/ctrace
