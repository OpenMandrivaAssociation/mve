%define snapshot 20220425
%define commit 354a652461377939ca136f451ba3271a1c52ee65
%define shortcommit %(c=%{commit}; echo ${c:0:7})

# FIXME: shaders path
#https://github.com/simonfuhrmann/mve/wiki/MVE-Users-Guide

Summary:	Multiple View Geometry
Name:		mve
Version:	0
Release:	1
Group:		Graphics
License:	BSD and GPLv3
Url:		https://www.gcc.tu-darmstadt.de/home/proj/mve/                
Source0:	https://github.com/simonfuhrmann/%{name}/archive/%{?snapshot:%{commit}}%{!?snapshot:%{version}}/%{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}.tar.gz

BuildRequires:	qmake5
BuildRequires:	doxygen
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
#BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Widgets)

%description
The Multi-View Environment is an effort to ease the work with multi-view
datasets and to support the development of algorithms based on multiple
views. It features Structure from Motion, Multi-View Stereo and Surface
Reconstruction.

MVE is developed at the TU Darmstadt.

%files
%license LICENSE.txt
%doc README.md
%doc docs/doxygen/html/
%{_bindir}/*
%dir %{_datadir}/u%{name}
%{_datadir}/u%{name}/shaders/
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/u%{name}*.xpm	
%{_iconsdir}/hicolor/*/apps/u%{name}*.png
#{_mandir}/man1/%{name}.1.*

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{commit}

# fix install (apps only)
sed -i -e "s|links:|install:|g" Makefile
sed -i -e "s|links:|install:|g" -e "s|ln -si|cp -a|g" Makefile apps/Makefile


%build
export CXXFLAGS="%{optflags} -std=c++17 -msse4.2"
%setup_compile_flags
%make_build

# umve
pushd apps/umve
%qmake_qt5
%make_build
popd

#docs
%make_build doc

%install
# NOTE: make install has any effects
install -dm 0755 %{buildroot}%{_bindir}/
BINDIR=%{buildroot}%{_bindir} %make_install

# shaders
install -dm 0755 %{buildroot}%{_datadir}/u%{name}/shaders/
install -pm 0644 apps/umve/shaders/* %{buildroot}%{_datadir}/u%{name}/shaders/

# icons
for i in 16 22 32 48 64 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/
	convert -scale ${i}x${i} apps/umve/images/icon_window.png \
			%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/u%{name}.png
done
#    pixmap
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -scale ${i}x${i} apps/umve/images/icon_window.png \
		%{buildroot}%{_datadir}/pixmaps/u%{name}.xpm

# .desktop
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat >%{buildroot}%{_datadir}/applications/%{vendor}-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
GenericName=Multiple View Geometry
Comment=A complete end-to-end pipeline for image-based geometry reconstruction
Exec=u%{name}
Icon=u%{name}
Terminal=false
Type=Application
Categories=Graphics;
EOF

