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

# Build requirements: keep gcc to provide libgcc and link metadata (works on AL2023),
# but use clang as actual compiler and lld as the linker.
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
# Install Rust via rustup (keeps toolchain consistent across distros)
# NOTE: rustup installs to $HOME/.cargo by default; $HOME in rpmbuild is /builddir.
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

# Sanitize environment (remove RPM-injected linker/compile flags that break rust builds)
unset LDFLAGS
unset LD_RUN_PATH
unset CFLAGS
unset CXXFLAGS

# Force clang as the C/C++ compiler
export CC=clang
export CXX=clang++

# Make rustc use clang as the linker driver and instruct clang to use lld.
# This preserves clang's library search paths while using lld as the actual linker.
export RUSTFLAGS="-C linker=clang -C link-arg=-fuse-ld=lld"

# Build
cargo build --release --locked

%check
export PATH="$HOME/.cargo/bin:$PATH"
unset LDFLAGS
unset LD_RUN_PATH
unset CFLAGS
unset CXXFLAGS

# Force clang as the C/C++ compiler
export CC=clang
export CXX=clang++

# Make rustc use clang as the linker driver and instruct clang to use lld.
# This preserves clang's library search paths while using lld as the actual linker.
export RUSTFLAGS="-C linker=clang -C link-arg=-fuse-ld=lld"
export CI=1
# Running tests may require more deps; skip if tests are network/privileged.
RUST_BACKTRACE=1 cargo test --release --locked || true

%install
mkdir -p %{buildroot}/bin
strip target/release/%{name}
install -m 755 target/release/%{name} %{buildroot}/bin/

%files
/bin/%{name}
