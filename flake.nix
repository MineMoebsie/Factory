{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.simpleFlake {
      inherit self nixpkgs;
      name = "MineMoebsie's factory game.";
      shell = ./shell.nix;
    };
}
