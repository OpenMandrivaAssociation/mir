# Force out of source build
%undefine __cmake_in_source_build

%ifnarch ppc64
# Enable LTO on non-ppc64 (c.f. rhbz#1515934)
%bcond_without lto
%endif

# Disable ctest run by default
# They take a long time and are generally broken in the build environment
%bcond_with run_tests

Name:           mir
Version:        2.16.4
Release:        1%{?dist}
Summary:        Next generation display server

# mircommon is LGPL-2.1-only/LGPL-3.0-only, everything else is GPL-2.0-only/GPL-3.0-only
License:        (GPL-2.0-only or GPL-3.0-only) and (LGPL-2.1-only or LGPL-3.0-only)
URL:            https://mir-server.io/
Source0:        https://github.com/MirServer/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  git-core
BuildRequires:  gcc-c++
BuildRequires:  cmake, ninja-build, doxygen, graphviz, lcov, gcovr
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  boost-devel
BuildRequires:  python3
BuildRequires:  glm-devel
BuildRequires:  glog-devel, lttng-ust-devel, systemtap-sdt-devel
BuildRequires:  gflags-devel
BuildRequires:  python3-pillow

# Everything detected via pkgconfig
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gbm) >= 9.0.0
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock) >= 1.8.0
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtest) >= 1.8.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml++-2.6)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(umockdev-1.0) >= 0.6
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-eglstream)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(yaml-cpp)
BuildRequires:  pkgconfig(wlcs)

# pkgconfig(egl) is now from glvnd, so we need to manually pull this in for the Mesa specific bits...
BuildRequires:  mesa-libEGL-devel

# For some reason, this doesn't get pulled in automatically into the buildroot
BuildRequires:  libatomic

# For detecting the font for CMake
BuildRequires:  gnu-free-sans-fonts

# For validating the desktop file for mir-demos
BuildRequires:  %{_bindir}/desktop-file-validate

# Add architectures as verified to work
%ifarch %{ix86} x86_64 %{arm} aarch64
BuildRequires:  valgrind
%endif


%description
Mir is a display server running on linux systems,
with a focus on efficiency, robust operation,
and a well-defined driver model.

%package devel
Summary:       Development files for Mir
Requires:      %{name}-common-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-server-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-lomiri-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-test-libs-static%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Documentation can no longer be built properly
Obsoletes:     %{name}-doc < 2.15.0

%description devel
This package provides the development files to create
applications that can run on Mir.

%package common-libs
Summary:       Common libraries for Mir
License:       LGPL-2.1-only or LGPL-3.0-only
# mirclient is gone...
Obsoletes:     %{name}-client-libs < 2.6.0
# debug extension for mirclient is gone...
Obsoletes:     %{name}-client-libs-debugext < 1.6.0
# mir utils are gone...
Obsoletes:     %{name}-utils < 2.0.0
# Ensure older mirclient doesn't mix in
Conflicts:     %{name}-client-libs < 2.6.0

%description common-libs
This package provides the libraries common to be used
by Mir clients or Mir servers.

%package lomiri-libs
Summary:       Lomiri compatibility libraries for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{name}-common-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-server-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description lomiri-libs
This package provides the libraries for Lomiri to use Mir
as a Wayland compositor.

%package server-libs
Summary:       Server libraries for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{name}-common-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description server-libs
This package provides the libraries for applications
that use the Mir server.

%package test-tools
Summary:       Testing tools for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{name}-server-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:    %{name}-demos
Recommends:    glmark2
Recommends:    xorg-x11-server-Xwayland
Requires:      wlcs
# mir-perf-framework is no more...
Obsoletes:     python3-mir-perf-framework < 2.6.0
# Ensure mir-perf-framework is not installed
Conflicts:     python3-mir-perf-framework < 2.6.0

%description test-tools
This package provides tools for testing Mir.

%package demos
Summary:       Demonstration applications using Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{name}-server-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      hicolor-icon-theme
Recommends:    xorg-x11-server-Xwayland
# For some of the demos
Requires:      gnu-free-sans-fonts

%description demos
This package provides applications for demonstrating
the capabilities of the Mir display server.

%package test-libs-static
Summary:       Testing framework library for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description test-libs-static
This package provides the static library for building
Mir unit and integration tests.


%prep
%autosetup -S git_am

# Drop -Werror
sed -e "s/-Werror//g" -i CMakeLists.txt


%build
%cmake	-GNinja %{?with_lto:-DMIR_LINK_TIME_OPTIMIZATION=ON} \
	-DMIR_USE_PRECOMPILED_HEADERS=OFF \
	-DCMAKE_INSTALL_LIBEXECDIR="usr/libexec/mir" \
	-DMIR_PLATFORM="gbm-kms;x11;wayland;eglstream-kms"

%cmake_build

%install
%cmake_install


%check
%if %{with run_tests}
# The tests are somewhat fiddly, so let's just run them but not block on them...
( %ctest ) || :
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/miral-shell.desktop


%files devel
%license COPYING.*
%{_bindir}/mir_wayland_generator
%{_libdir}/libmir*.so
%{_libdir}/pkgconfig/mir*.pc
%{_includedir}/mir*

%files common-libs
%license COPYING.LGPL*
%doc README.md
%{_libdir}/libmircore.so.*
%{_libdir}/libmircommon.so.*
%{_libdir}/libmircookie.so.*
%{_libdir}/libmirplatform.so.*
%dir %{_libdir}/mir

%files lomiri-libs
%license COPYING.GPL*
%doc README.md
%{_libdir}/libmiroil.so.*

%files server-libs
%license COPYING.GPL*
%doc README.md
%{_libdir}/libmiral.so.*
%{_libdir}/libmirserver.so.*
%{_libdir}/libmirwayland.so.*
%dir %{_libdir}/mir/server-platform
%{_libdir}/mir/server-platform/graphics-eglstream-kms.so.*
%{_libdir}/mir/server-platform/graphics-gbm-kms.so.*
%{_libdir}/mir/server-platform/graphics-wayland.so.*
%{_libdir}/mir/server-platform/input-evdev.so.*
%{_libdir}/mir/server-platform/renderer-egl-generic.so.*
%{_libdir}/mir/server-platform/server-virtual.so.*
%{_libdir}/mir/server-platform/server-x11.so.*

%files test-tools
%license COPYING.GPL*
%{_bindir}/mir-*test*
%{_bindir}/mir_*test*
%dir %{_libdir}/mir/tools
%{_libdir}/mir/tools/libmirserverlttng.so
%dir %{_libdir}/mir
%{_libdir}/mir/miral_wlcs_integration.so
%dir %{_libdir}/mir/server-platform
%{_libdir}/mir/server-platform/graphics-dummy.so
%{_libdir}/mir/server-platform/input-stub.so

%files test-libs-static
%license COPYING.GPL*
%{_libdir}/libmir-test-assist.a

%files demos
%license COPYING.GPL*
%doc README.md
%{_bindir}/mir_demo_*
%{_bindir}/miral-*
%{_datadir}/applications/miral-shell.desktop
%{_datadir}/icons/hicolor/scalable/apps/ubuntu-logo.svg
