# QA Automation Framework - Sauce Demo

A professional QA automation testing framework built with Python, Pytest, and Playwright, demonstrating best practices in test automation including the Page Object Model (POM) pattern.

## Project Overview

This framework automates end-to-end testing of the [Sauce Demo](https://www.saucedemo.com) web application, covering:

- User authentication (login/logout)
- Product inventory browsing and sorting
- Shopping cart operations
- Complete checkout flow

## Tech Stack

- **Python 3.10+** - Programming language
- **Playwright** - Browser automation
- **Pytest** - Test framework
- **pytest-html** - HTML reporting
- **Allure** - Advanced reporting
- **pipenv** - Virtual environment and dependency management

## Project Structure

```
QA/
├── config/              # Configuration settings
│   └── settings.py      # Environment configuration
├── data/                # Test data files
│   ├── checkout.csv     # Checkout form test data
│   ├── checkout.json    # Checkout form test data (JSON)
│   ├── products.json    # Product data
│   ├── users.csv        # User credentials test data
│   └── users.json       # User credentials test data (JSON)
├── logs/                # Test execution logs
├── pages/               # Page Object Model classes
│   ├── base_page.py     # Base page with common methods
│   ├── cart_page.py     # Shopping cart page
│   ├── checkout_page.py # Checkout pages (step 1, 2, complete)
│   ├── inventory_page.py# Product listing page
│   └── login_page.py    # Login page
├── reports/             # Test reports and artifacts
│   └── artifacts/       # Screenshots, videos, traces
├── tests/               # Test files
│   ├── test_cart.py     # Shopping cart tests
│   ├── test_checkout.py # Checkout flow tests
│   ├── test_inventory.py# Product inventory tests
│   └── test_login.py    # Login functionality tests
├── utils/               # Utility modules
│   ├── data_loader.py   # Test data loading utilities
│   ├── helpers.py       # Helper functions
│   └── logger.py        # Logging configuration
├── .env                 # Environment variables
├── conftest.py          # Pytest fixtures
├── pytest.ini           # Pytest configuration
├── Pipfile              # Pipenv dependencies
├── Pipfile.lock         # Locked dependencies
└── requirements.txt     # Requirements for pip
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pipenv (`pip install pipenv`)

### Setup

1. Clone the repository and start the virtual environment:
```bash
git clone https://github.com/your-username/qa-playwright.git
cd qa-playwright
pipenv shell
```

2. Install dependencies:
```bash
pipenv install
```

3. Install Playwright browsers:
```bash
pipenv run playwright install chromium
```

### Alternative: Using pip

```bash
pip install -r requirements.txt
playwright install chromium
```

## Running Tests

### Run all tests
```bash
pipenv run pytest
```

### Run specific test file
```bash
pipenv run pytest tests/test_login.py
```

### Run tests by marker
```bash
# Smoke tests
pipenv run pytest -m smoke

# Login tests
pipenv run pytest -m login

# Negative tests
pipenv run pytest -m negative

# End-to-end tests
pipenv run pytest -m e2e
```

### Run in headless mode
```bash
pipenv run pytest --headless
```

### Run with specific browser
```bash
pipenv run pytest --browser chromium
pipenv run pytest --browser firefox
pipenv run pytest --browser webkit
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Critical path tests for quick validation |
| `regression` | Full regression test suite |
| `login` | Login functionality tests |
| `inventory` | Product inventory tests |
| `cart` | Shopping cart tests |
| `checkout` | Checkout flow tests |
| `negative` | Negative/error scenario tests |
| `e2e` | End-to-end flow tests |

## Reports

### HTML Report
After test execution, find the HTML report at:
```
reports/report.html
```

### Allure Report
Generate Allure report:
```bash
pipenv run pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Screenshots and Videos
Artifacts (screenshots, videos, traces) are saved to:
```
reports/artifacts/
```

## Configuration

### Environment Variables (.env)

```env
BASE_URL=https://www.saucedemo.com
STANDARD_USER=standard_user
PASSWORD=secret_sauce
HEADLESS=false
SLOW_MO=100
TIMEOUT=30000
```

### Pytest Configuration (pytest.ini)

The `pytest.ini` file contains:
- Browser settings (chromium, headed mode)
- Screenshot/video capture settings
- Logging configuration
- Test markers

## Page Object Model (POM)

This framework follows the POM pattern for better maintainability:

### BasePage
Contains common methods inherited by all pages:
- Navigation (`navigate`, `reload`, `go_back`)
- Element interactions (`click`, `fill`, `select_option`)
- Waits (`wait_for_element`, `wait_for_url`)
- Assertions (`expect_visible`, `expect_text`)

### Page-specific Classes
Each page has:
- **Locators class**: CSS selectors separated from logic
- **Page class**: Actions and verifications specific to that page

Example:
```python
from pages.login_page import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    login_page.expect_login_successful()
```

## Test Data Management

### JSON Format
```json
{
  "valid_users": [
    {"username": "standard_user", "password": "secret_sauce"}
  ]
}
```

### CSV Format
```csv
username,password,expected_result
standard_user,secret_sauce,success
```

### Usage in Tests
```python
from utils.data_loader import DataLoader

@pytest.mark.parametrize("user", DataLoader.get_valid_users())
def test_login(login_page, user):
    login_page.login(user["username"], user["password"])
```

## Fixtures

Key fixtures defined in `conftest.py`:

| Fixture | Description |
|---------|-------------|
| `login_page` | LoginPage instance |
| `inventory_page` | InventoryPage instance |
| `cart_page` | CartPage instance |
| `logged_in_page` | Pre-authenticated page |
| `logged_in_inventory` | Inventory page with logged-in user |
| `cart_with_one_item` | Cart with one product |
| `cart_with_multiple_items` | Cart with three products |
| `valid_users` | Valid user test data |
| `invalid_users` | Invalid user test data |

## Best Practices Implemented

1. **Page Object Model**: Separation of page structure and test logic
2. **Data-Driven Testing**: Test data externalized in JSON/CSV files
3. **Fixtures**: Reusable test setup with pytest fixtures
4. **Markers**: Organized test categorization
5. **Logging**: Comprehensive logging for debugging
6. **Configuration**: Environment-based configuration
7. **DRY Principle**: No code duplication
8. **Type Hints**: Full type annotations for better IDE support

## Continuous Integration

Example GitHub Actions workflow:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install pipenv
          pipenv install
          pipenv run playwright install chromium
      - name: Run tests
        run: pipenv run pytest --headless
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports
          path: reports/
```

## License

MIT License

## Author

QA Automation Engineer

---

*This project demonstrates professional QA automation skills using modern Python testing tools and best practices.*
