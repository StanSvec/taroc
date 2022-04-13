# Error Codes

## ERR1: Invalid Configuration - SSH is disabled
At the moment the client supports only SSH communication for connecting to the hosts. Therefore, SSH config must be enabled.
Check that `ssh_config.enabled` is set to `true` in `taroc.yaml` config file or use `--set ssh_config_enabled=true` CLI option.

## ERR2: Invalid Configuration Attribute
**Check that your configuration file and `--set` options are correct.**

The configuration is stored in predefined attributes of [cfg module](taroc/cfg.py). The set of initial values is called minimal configuration.
Unless specified otherwise, the configuration file `taro.yaml` is loaded during initialization phase and its values are set to the attributes of `cfg` module.
The attributes of `cfg` module can be also overridden by `--set` CLI options in taroc application.
This error occurs when a configuration attribute to set does not exist.
