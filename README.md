![PyPI - Version](https://img.shields.io/pypi/v/UAForge?style=for-the-badge&labelColor=%234f4f4d&color=%23c4ff03&link=https%3A%2F%2Fpypi.org%2Fproject%2FUAForge%2F)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/UAForge?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/UAForge?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fbolgac%2FUAForge%2Fblob%2Fmain%2FLICENSE)

---
# UAForge - UserAgent Generator

A powerful Python library and CLI tool for generating realistic, random user agent strings for Chrome, Firefox, and Opera browsers across multiple platforms.

---

## Features
- **Multi-browser support**: Generate user agents for Chrome, Firefox, and Opera  
- **Cross-platform**: Supports Windows, Linux, macOS, Android, and iOS  
- **Real version data**: Uses real browser version information from official sources  
- **Realistic combinations**: Creates plausible user agent strings that mimic real browsers  
- **SQLite database**: Stores version data locally for fast access  
- **Auto-update**: Fetch latest browser versions from official sources  
- **CLI interface**: Easy command-line usage  
- **Python API**: Simple integration into Python projects  

---

## Installation

### From PyPI (Recommended)
```bash
pip install uaforge
```

## Quick Start

### Using the CLI

Initialize the database (first-time setup):
```bash
uaforge --init
```
Generate a single user agent:
```bash
# Random browser user agent
uaforge

# Specific browser
uaforge --browser Chrome
uaforge --browser Firefox
uaforge --browser Opera

# Generate 10 Chrome user agents
uaforge --count 10 --browser Chrome

# Save to file
uaforge --count 50 --output useragents.txt --browser Firefox
```

Update browser versions:
```bash
# Update all versions
uaforge --update all

# Update specific browser
uaforge --update chrome
uaforge --update firefox
uaforge --update opera
uaforge --update android
uaforge --update mac
```

### Using Python API

```bash
from uaforge import generate_user_agent, generate_multiple, update_versions

# Generate a single user agent
ua = generate_user_agent("Chrome")
print(ua)

# Generate multiple user agents
ua_list = generate_multiple(5)
for agent in ua_list:
    print(agent)

# Update browser versions
update_versions("all")
```

### Advanced Usage
```bash
from uaforge.core.user_agent import UserAgentGenerator

# Create a custom generator
generator = UserAgentGenerator()

# Generate specific types
chrome_agent = generator.create_useragent("Chrome")
firefox_agent = generator.create_useragent("Firefox")
opera_agent = generator.create_useragent("Opera")

# Get a batch of agents
agents = generator.get_list(100)
```

### Command Line Reference

| Option | Short | Description |
|--------|-------------|-------------|
|--count | -c | Number of user agents to generate (default: 1) |
|--browser | -b | Browser type: Chrome, Firefox, Opera, random (default: random) |
|--output | -o | Output file to save user agents |
|--update | -u | Update version information: all, chrome, firefox, opera, android, windows, linux, mac |
|--init |  | Initialize database with initial data |
|--version | -v | Show version information |

---

## Examples
```bash
# Show version
uaforge --version

# Initialize database
uaforge --init

# Update all versions
uaforge --update all

# Generate 5 Firefox user agents
uaforge --count 5 --browser Firefox

# Generate 100 random user agents and save to file
uaforge --count 100 --output agents.txt

# Generate a single Chrome user agent
uaforge --browser Chrome
```

## Database Structure
- **Browser versions:** Chrome, Firefox, Opera version history
- **Platform information:** Windows, Linux, macOS, Android system strings
- **Version types:** Architecture and build types for each platform
- **Release dates:** Version release information
- **Database location:** ~/.useragent_generator/data/useragent.db

---

## Supported Platforms and Browsers

**Browsers**
- Google Chrome (desktop & mobile)
- Mozilla Firefox (desktop & mobile)
- Opera (desktop & mobile)

**Operating Systems**
- Windows (NT 6.0 to NT 10.0)
- Linux (X11 variants)
- macOS (10.15 to 14.0)
- Android (10 to 14)
- iOS (simulated via macOS strings)

**Architectures**
- Windows: x64, WOW64
- Linux: i686, x86_64
- Android: armv7l, armv8l

---

## Project Structure
```bash
uaforge/
├── core/
│   ├── __init__.py        # init file
│   ├── database.py        # SQLite database operations
│   ├── user_agent.py      # Main user agent generator
│   ├── version_fetcher.py # Fetch versions from web
│   └── version_updater.py # Update database with new versions
├── cli.py                 # Command-line interface
├── utils.py               # Utility functions
└── __init__.py            # Package exports
```

## Development
```bash
# Clone the repository
git clone https://github.com/bolgac/uaforge.git
cd uaforge

# Install in development mode
pip install -e .[dev]

# Run tests
python -m pytest

# Build distribution
python setup.py sdist bdist_wheel
```

## Common Issues and Solutions
### Database Not Found

```bash
uaforge --init
```
### Empty User Agents

```bash
uaforge --update all
```
### Network Issues
- Check your internet connection
- Use --init for offline mode with sample data
- Configure proxy if needed

### Permission Errors
- Run with appropriate permissions
- Check database file permissions

---

## Contributing

Feel free to fork this project, submit PRs, or suggest features via GitHub Issues!

We welcome contributions of all kinds:
- Bug reports and fixes
- New features and enhancements
- Documentation improvements
- Testing and code quality improvements

---

## Support This Project

If this tool helps you save time or enhances your projects, consider showing some ❤️ to support its further development:

### Donate

- **USDT (TRC20)**: `T9zmkRHR49PKNgi2GvFReWzoX6mxvXwCwQ`
- **BTC**: `3FiGD5moqSctBY93h11H3TvPncWLCe5up5`  
- **Ethereum (ERC20)**: `0xac25c934e64a95ba38a5ca2c8ca149c8bf13eaa3`  
- **TRX (TRC20)**: `T9zmkRHR49PKNgi2GvFReWzoX6mxvXwCwQ`  

### Become a Sponsor

Get early access to premium features and sponsor-only tools. Contact us for sponsor tiers and benefits.

---

## Contact

- GitHub Issues – for bugs and feedback  
- Email – `bytearchsoft@gmail.com` (for business inquiries or sponsorships)

---

## License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Browser version data from official sources:

    - [Chrome](https://chromedriver.storage.googleapis.com/)
    - [Firefox](https://www.mozilla.org/en-US/firefox/releases/)
    - [Android](https://tr.wikipedia.org/wiki/Android)
    - [Opera](https://blogs.opera.com/desktop/)
    - [Mac-Wikipedia](https://en.wikipedia.org/wiki/)

- Inspired by various user agent generation libraries
- Contributors and testers

---
