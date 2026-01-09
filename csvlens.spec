%define name csvlens
%define version 0.15.1
%define release 1%{?dist}

Summary:  Command line csv viewer
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT
URL:      https://github.com/YS-L/csvlens
Source0:  https://github.com/YS-L/csvlens/archive/refs/tags/v%{version}.tar.gz

%define debug_package %{nil}
%global _package_note_flags %{nil}
%undefine _package_note_ldflags

BuildRequires: curl
BuildRequires: gcc
BuildRequires: clang
BuildRequires: lld
BuildRequires: glibc-devel

%description
csvlens is a command line CSV file viewer. It is like less but made for CSV.

%prep
%setup -q -n csvlens-%{version}

%build
# Install Rust using rustup (consistent across distros)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

# Force a stable, portable toolchain
export CC=clang
export CXX=clang++
export RUSTFLAGS="-C linker=clang -C link-arg=-fuse-ld=lld"

cargo build --release --locked

%check
export PATH="$HOME/.cargo/bin:$PATH"
export CI=1
cargo test --release --locked

%install
mkdir -p %{buildroot}/bin
strip target/release/%{name}
install -m 755 target/release/%{name} %{buildroot}/bin/

%files
/bin/%{name}
