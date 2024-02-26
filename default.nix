{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python3.pkgs;

in pythonPackages.buildPythonApplication rec {
  pname = "myshop";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = with pythonPackages; [
    gunicorn
  ];

  # Optionally, you can add system dependencies here
  nativeBuildInputs = with pkgs; [
    gcc
    pango
    libjpeg
    libopenjp2
    libffi
    glib
  ];

  meta = with pkgs.stdenv.lib; {
    description = "MyShop application";
    license = licenses.mit;
    platforms = platforms.all;
  };
}
