{ pkgs, lib, config, inputs, ... }:

{
  # Environment variables
  env = {
    LD_LIBRARY_PATH = "$NIX_LD_LIBRARY_PATH:$LD_LIBRARY_PATH";
  };

  # Packages
  packages = [
    pkgs.uv
    pkgs.nushell
    pkgs.convco
    pkgs.trufflehog
  ];

  # Python language configuration
  languages.python = {
    enable = true;
    package = pkgs.python312;
    uv = {
      enable = true;
      sync.enable = false; # pyproject.toml is located under collector/
    };
  };

  # Helper scripts
  scripts = {
    nu-shell.exec = "exec nu";
    test-collector.exec = "cd collector && uv run pytest";
    lint-collector.exec = "cd collector && uv run ruff check . && uv run ruff format --check .";
    check-all.exec = "lint-collector && cd collector && uv run mypy src";
  };

  # Git hooks integration
  git-hooks.hooks = {
    check-added-large-files.enable = true;
    check-yaml = {
      enable = true;
      excludes = [ "chart/templates/.*" ];
    };
    convco.enable = true;
    end-of-file-fixer.enable = true;
    fix-byte-order-marker.enable = true;
    trim-trailing-whitespace.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;

    typos = {
      enable = true;
      excludes = [ "collector/src/db/migrations/versions/.*" ];
    };

    trufflehog = {
      enable = true;
      stages = [ "pre-push" ];
    };

    # App-specific hooks for collector
    mypy-collector = {
      enable = true;
      name = "mypy collector";
      stages = [ "pre-push" ];
      files = "^collector/";
      entry = "sh -c 'cd ./collector && uv run mypy .'";
      pass_filenames = false;
    };

    ty-collector = {
      enable = true;
      name = "ty collector check";
      files = "^collector/";
      entry = "sh -c 'cd ./collector && uvx ty check'";
      types = [ "python" ];
      pass_filenames = false;
    };
  };
}
