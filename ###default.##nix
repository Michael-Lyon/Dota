{ pkgs ? import <nixpkgs> {} }:

let
 pythonPackages = pkgs.python3.pkgs;

in pythonPackages.buildPythonApplication rec {
 pname = "myshop";
 version = "0.1";

 src = ./.;

 propagatedBuildInputs = with pythonPackages; [
   gunicorn
   gobject-introspection  # Added for GObject support
   pycairo  # Cairo graphics library
   pygobject3  # Python bindings for GObject
 ];

 # Expanded system dependencies
 nativeBuildInputs = with pkgs; [
   gcc
   pango
   libjpeg
   libopenjp2
   libffi
   glib
   gobject-introspection
   pkg-config
   zlib
   libxml2
   cairo
 ];

 # Add a configure phase to potentially optimize build
 configurePhase = ''
   export PYTHONOPTIMIZE=2
   export GI_TYPELIB_PATH=${pkgs.gobject-introspection}/lib/girepository-1.0
 '';

 # Optional: Add post-install script for additional setup
 postInstall = ''
   mkdir -p $out/bin
   # Create a wrapper script for gunicorn with optimized settings
   cat > $out/bin/myshop-gunicorn <<EOF
#!/bin/sh
exec ${pythonPackages.gunicorn}/bin/gunicorn \\
 --workers 2 \\
 --timeout 120 \\
 --max-requests 1000 \\
 --max-requests-jitter 50 \\
 myshop.wsgi:application
EOF
   chmod +x $out/bin/myshop-gunicorn
 '';

 meta = with pkgs.lib; {
   description = "MyShop application";
   license = licenses.mit;
   platforms = platforms.linux;
 };
}