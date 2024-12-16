{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python3.pkgs;

in pythonPackages.buildPythonApplication rec {
  pname = "myshop";
  version = "0.1";

  src = ./.;

  # Add more Python dependencies that might be critical
  propagatedBuildInputs = with pythonPackages; [
    gunicorn
    # Consider adding these if not already in requirements.txt
    # django
    # psycopg2  # if using PostgreSQL
    # celery  # if using background tasks
  ];

  # Expanded system dependencies
  nativeBuildInputs = with pkgs; [
    gcc
    pango
    libjpeg
    libopenjp2
    libffi
    glib
    pkg-config  # helps with library detection
    zlib  # common dependency
  ];

  # Add a configure phase to potentially optimize build
  configurePhase = ''
    export PYTHONOPTIMIZE=2  # Enable more aggressive optimizations
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
    platforms = platforms.linux;  # More specific platform targeting
  };
}