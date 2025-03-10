%define name csvlens
%define version 0.12.0
%define release 1%{?dist}

Summary:  Command line csv viewer
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT license
URL:      https://github.com/YS-L/csvlens
Source0:  https://github.com/YS-L/csvlens/archive/refs/tags/v%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: curl
BuildRequires: gcc

%description
csvlens is a command line CSV file viewer. It is like less but made for CSV.

%prep
%setup -q -n csvlens-%{version}
cat <<EOF | patch -p0
--- src/app.rs  2025-03-10 09:21:08.728286972 +0200
+++ src/app.rs  2025-03-10 09:23:17.238121646 +0200
@@ -2354,7 +2354,9 @@
             &mut terminal,
             Control::FilterColumns("COL1".into()),
         );
+        till_app_ready(&app);
         step_and_draw(&mut app, &mut terminal, Control::Filter("x1".into()));
+        till_app_ready(&app);
         // Toggle to cell selection
         step_and_draw(&mut app, &mut terminal, Control::ToggleSelectionType);
         step_and_draw(&mut app, &mut terminal, Control::ToggleSelectionType);
EOF

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release --locked

%check
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
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
