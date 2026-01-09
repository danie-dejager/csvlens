%define name csvlens
%define version 0.15.1
%define release 1%{?dist}

Summary:  Command line csv viewer
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT license
URL:      https://github.com/YS-L/csvlens
Source0:  https://github.com/YS-L/csvlens/archive/refs/tags/v%{version}.tar.gz

%define debug_package %{nil}
%global _package_note_flags %{nil}
%undefine _package_note_ldflags

BuildRequires: curl
BuildRequires: gcc

%description
csvlens is a command line CSV file viewer. It is like less but made for CSV.

%prep
%setup p1 -q -n csvlens-%{version}

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release --locked

%check
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
export CI=1
RUST_BACKTRACE=1 cargo test --release --locked

%install
# Create the necessary directory structure in the buildroot
mkdir -p %{buildroot}/bin

# Copy the binary to /bin in the buildroot
strip target/release/%{name}
install -m 755 target/release/%{name} %{buildroot}/bin/

%files
# List all the files to be included in the package
/bin/%{name}
