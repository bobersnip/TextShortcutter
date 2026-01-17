# TextShortcutter - Secure Text Expander

A Python-based text expander application that activates only with a configurable keybind. Features a GUI for managing shortcuts and a popup for selecting expansions.

## Features

### 🔧 **Core Functionality**
- **Configurable Trigger Key**: Default is `Ctrl+Space`, but you can set any key combination
- **Text Expansion**: Convert short text like "omg" into "Oh my gosh!"
- **Popup Selection**: When trigger is pressed, a popup shows all available expansions
- **Clipboard Integration**: Smart clipboard handling to paste expansions without losing original content

### 🛡️ **Security Features**
- **Trigger Key Protection**: Expansions only activate with explicit user action
- **Application Filtering**: Configure safe/blocked applications
- **Privacy Mode**: Enhanced security with reduced logging
- **Secure Storage**: Encrypted configuration and expansion storage

### 🎨 **User Interface**
- **Modern GUI**: Clean, intuitive interface for managing expansions
- **Real-time Search**: Filter expansions while selecting
- **Usage Statistics**: Track how often each expansion is used
- **Import/Export**: Easily backup and share your expansions

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python src/main.py
   ```

3. **Or Install as Package**
   ```bash
   pip install -e .
   textshortcutter
   ```

## Usage

### Adding Expansions
1. Open the application
2. In the "Add New Expansion" section:
   - Enter a shortcut (e.g., "omg")
   - Enter the expansion text (e.g., "Oh my gosh!")
   - Add an optional description
3. Click "Add Expansion"

### Using Expansions
1. Press your configured trigger key (default: `Ctrl+Space`)
2. A popup will appear showing all available expansions
3. Use keyboard navigation (Up/Down arrows) or mouse to select
4. Press Enter or double-click to paste the selected expansion
5. Use the search box to filter expansions

### Configuration
- **Trigger Key**: Change in the "Trigger Configuration" section
- **Security Level**: Adjust security settings (1-10)
- **Privacy Mode**: Enable for enhanced security

## Security

### Keylogger Protection
- **Explicit Activation**: Expansions only work when you press the trigger key
- **No Background Monitoring**: No constant keyboard monitoring for shortcuts
- **Secure Clipboard**: Original clipboard content is preserved

### Data Protection
- **Local Storage**: All data stored locally on your machine
- **Encrypted Config**: Configuration files are encrypted
- **No Network Access**: Application doesn't require internet access

## File Structure

```
TextShortcutter/
├── src/
│   └── main.py              # Main application
├── requirements.txt          # Python dependencies
├── setup.py                # Package setup
├── test_basic.py           # Basic functionality tests
├── README_PROJECT.md       # This file
└── docs/                   # Documentation (future)
```

## Configuration Files

The application stores configuration and expansions in:
- **Windows**: `%APPDATA%\textshortcutter\`
- **macOS**: `~/Library/Application Support/textshortcutter/`
- **Linux**: `~/.textshortcutter/`

Files:
- `config.json` - Application settings
- `expansions.json` - Your text expansions
- `app.log` - Application logs

## Development

### Running Tests
```bash
python test_basic.py
```

### Building Package
```bash
python setup.py sdist bdist_wheel
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Trigger key not working:**
- Check that no other application is using the same key combination
- Try changing the trigger key in settings
- Ensure the application has necessary permissions

**Expansions not pasting:**
- Check that you're in a text field where pasting is allowed
- Try the "Test Selected Expansion" feature to verify functionality
- Check application logs for errors

### Getting Help

- Check the application logs in the config directory
- Ensure you have the latest version
- Report issues on the [GitHub repository](https://github.com/bobersnip/TextShortcutter)

## License

This project is proprietary software owned by Convenience Culture LLC. All rights reserved.

**Commercial Use Prohibited**: This software cannot be used, modified, or distributed for commercial purposes without explicit written permission.

**Development License**: For development and testing purposes only.

## Security Notice

While TextShortcutter implements multiple security measures, no software can be completely secure. Users are responsible for:
- Setting appropriate security levels for their environment
- Regularly reviewing audit logs
- Using strong application filtering
- Following security best practices

Always keep your system and applications updated with the latest security patches.
