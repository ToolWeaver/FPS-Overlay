# FPS Overlay

A customizable, always-on-top FPS (Frames Per Second) counter overlay for Windows applications, built with PyQt5.



## Features

- **Always-on-top display**: Monitor your FPS while running any application
- **Highly customizable appearance**:
  - Text color and font
  - Background color with opacity control
  - Optional gradient background
  - Border style, width, and color
  - Drop shadow effects
  - Fully transparent mode
- **Interactive edit mode**: Easily reposition and resize the overlay
- **Convenient keyboard shortcuts**:
  - `Ctrl+E`: Toggle edit mode
  - `Ctrl+S`: Open settings dialog

## Requirements

- Python 3.6+
- PyQt5

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install PyQt5
```

## Usage

Run the application:

```bash
python main.py
```

### Basic Controls

- The overlay will appear in the top-right corner of your screen by default
- Press `Ctrl+E` to enter edit mode (green dashed border will appear)
- In edit mode:
  - Click and drag to move the overlay
  - Drag from the bottom-right corner to resize
- Press `Ctrl+E` again to exit edit mode
- Press `Ctrl+S` to open the settings dialog

### Customization Options

The settings dialog offers extensive customization:

- **Text**: Change color and font
- **Background**: 
  - Adjust color and opacity
  - Enable gradient background with customizable colors
  - Enable fully transparent mode (text only)
- **Border**: Customize style, width, and color
- **Shadow**: Add drop shadow with adjustable color, blur radius, and offset
- **Layout**: Adjust padding

## How It Works

The application creates a frameless, always-on-top window that calculates and displays the current FPS. By default, it's transparent to mouse events, allowing you to interact with applications underneath it.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgements

Built with PyQt5, a set of Python bindings for Qt application framework. 