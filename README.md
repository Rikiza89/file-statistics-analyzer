# File Statistics Analyzer

A comprehensive Python GUI application built with Tkinter that provides detailed statistical analysis of any text-based file.

## Features

### Core Statistics
- **File Information**: Size, encoding, BOM detection, line endings (CRLF/LF/CR)
- **Time Metadata**: Creation, modification, and access timestamps
- **Character Analysis**: Total characters, alphabetic, numeric, uppercase, lowercase, special chars, non-ASCII
- **Line Statistics**: Total, empty, non-empty lines, length metrics, PEP 8 compliance checks
- **Word Statistics**: Total/unique words, lexical diversity, word length analysis
- **Indentation**: Indented lines count, average and maximum indentation depth
- **Punctuation**: Commas, periods, semicolons, colons, and more
- **Brackets & Quotes**: All types with open/close counts
- **Code Structure**: Maximum nesting depth

### Advanced Analysis
- **Readability Metrics**: Flesch Reading Ease score, sentence analysis
- **Top Frequencies**: Most common words and characters
- **Code Quality**: Trailing whitespace, long lines detection

### Language-Specific Features

**Python (.py)**
- Functions, classes, decorators
- Import statements, comments, docstrings
- F-strings, list comprehensions
- Try-except blocks, type hints
- TODO/FIXME/NOTE comments
- String literal analysis

**HTML (.html, .htm)**
- Tag counts (div, script, style, img, anchor)
- Attributes, comments

**CSS (.css)**
- Selectors, properties, media queries
- Unique classes and IDs

**JavaScript (.js)**
- Function types (regular, arrow)
- Variable declarations (var, let, const)
- Comments, template literals

**JSON (.json)**
- Validation, nesting depth, key count

**XML (.xml)**
- Tags, self-closing tags, comments

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Installation

```bash
git clone https://github.com/Rikiza89/file-statistics-analyzer.git
cd file-statistics-analyzer
```

## Usage

```bash
python stats_app_1.py
```

1. Click "Browse File" button
2. Select any text-based file
3. View comprehensive statistics instantly

## Supported File Types

All text-based files including:
- `.py` (Python)
- `.html`, `.htm` (HTML)
- `.css` (CSS)
- `.js` (JavaScript)
- `.json` (JSON)
- `.xml` (XML)
- `.txt` (Text)
- And more...

## Screenshots

The application provides a clean, scrollable interface displaying:
- Organized sections with clear headers
- Detailed metrics with proper formatting
- Language-specific statistics based on file type

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Rikiza89

## Acknowledgments

Built with Python and Tkinter for cross-platform compatibility.
