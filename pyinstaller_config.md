# External Configuration with PyInstaller

When building executables with PyInstaller, particularly using the `--onefile` option, there are specific considerations for external configuration files.

## How It Works Now

The fixed implementation handles external configuration correctly:

1. The executable will look for `hue_config.json` in the **same directory as the executable**, not in the PyInstaller temp directory.

2. If the file is not found, it will create a default configuration file in that location.

3. Changes to the configuration file will be detected each time the application starts.

## Building the Executable

Use the updated spec file:
```
pyinstaller hue.spec
```

This creates a standalone executable that correctly uses external configuration.

## IMPORTANT: No Bundled Config

With the updated approach:

1. The config file is NOT bundled inside the executable
2. A template config is created in the build directory, but only for reference
3. You must copy a configuration file to the same directory as the executable

## Testing External Configuration

To verify external configuration is working:

1. Build the executable: `pyinstaller hue.spec`
2. Copy `hue_config.json` to the same directory as the executable in `dist/`
3. Run the executable and verify it loads your config (watch the console output)
4. Make a change to the JSON file
5. Restart the executable and verify it picks up your changes

## Troubleshooting

If configuration changes still aren't detected:

1. Check if the application has permission to read/write in its directory
2. Look at console output for paths (where it's looking for the config)
3. Verify JSON file syntax is valid
4. Try running the executable with administrator privileges once

## Setting Up as a Service

When setting up as a Windows service or scheduled task, make sure:

1. The working directory is set to the executable's directory
2. The account running the task has read/write permissions
