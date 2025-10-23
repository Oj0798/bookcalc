# Book Calculation Application

## Overview

This is a Flask-based web application designed to calculate printing costs for multiple books with worldwide accessibility. The application helps users determine material costs by considering various paper sizes, final book dimensions, currency conversions, and regional shipping costs. It supports Arabic language (RTL layout) and 10 international currencies, making it suitable for global publishing cost estimation.

The core functionality calculates how many reference sheets are needed based on the final book size, applies multipliers for different trimmed sizes, and provides comprehensive cost breakdowns with currency conversion and regional shipping rates.

**Recent Update (October 2025):** Added worldwide/global functionality including multi-currency support, regional shipping zones, and production-ready deployment configuration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- HTML5 with Arabic language support (RTL - right-to-left layout)
- Client-side JavaScript for dynamic form manipulation
- CSS for styling and responsive design

**Key Design Decisions:**
- RTL layout to support Arabic language users
- Dynamic form generation allowing users to add multiple books to a single calculation
- Grouped dropdown options (optgroups) organizing book sizes by paper family (70×100, 82×57, 90×60)

**Rationale:** The RTL design and Arabic language support indicate this application targets Middle Eastern publishing markets. The dynamic form approach allows batch calculations without page refreshes, improving user experience.

### Backend Architecture

**Framework:** Flask (Python)
- Minimal web framework chosen for simplicity and rapid development
- Template rendering using Jinja2 (Flask's default templating engine)
- Custom template folder configuration (`template_folder='bookcalculation'`)

**Application Structure:**
- Single-file application (`main.py`) containing all business logic
- Route handlers:
  - `/` - Renders the input form
  - `/calculate_multiple` - Processes POST requests for cost calculations

**Core Business Logic:**
The application implements a multiplier-based calculation system:
- Base reference sheet sizes (0.57×0.82m, 0.60×0.90m, 0.70×1.00m)
- Final size multipliers organized by paper families
- Three paper families with different standard sizes and multiplier scales
- Multipliers range from 0.25× (smaller formats) to 4.0× (larger formats)

**Rationale:** The single-file approach is suitable for this application's scope. The multiplier system allows flexible calculations across different paper families while maintaining consistency in pricing logic.

### Data Architecture

**In-Memory Data Structures:**
- `paper_sizes` (list): Reference sheet dimensions
- `final_size_multipliers` (dictionary): Maps final book sizes to calculation multipliers
- `currency_rates` (dictionary): Exchange rates and currency metadata

**Data Model:**
Each currency entry contains:
- `symbol`: Display symbol for the currency
- `rate`: Exchange rate relative to USD
- `name`: Full currency name

Supported currencies include: USD, EUR, GBP, AED, SAR, EGP, JPY, CNY, INR, TRY

**Regional Shipping Zones:**
- `regional_shipping` (dictionary): Maps shipping regions to cost per kg
- Supported regions: Local, Middle East, North Africa, Europe, Asia, North America, South America, Africa, Oceania
- Each region has different per-kg shipping costs ranging from $0.1 (Local) to $2.0 (Oceania)

**Rationale:** In-memory data structures are appropriate for this application as the data is static configuration rather than dynamic user data. No persistent storage is needed for the calculation logic itself.

### Calculation Engine

**Multiplier System:**
The application uses a three-tier paper family system:
1. **70×100 family** - Standard sizes: 17×24cm (1.0×), scaling up to 50×35cm (4.0×) and down to 6×8cm (0.25×)
2. **82×57 family** - Standard sizes: 14×20cm (1.0×), scaling up to 40×28cm (4.0×) and down to 7×10cm (0.25×)
3. **90×60 family** - Standard sizes: 15×22cm (1.0×), scaling up to 45×30cm (4.0×) and down to 7.5×11cm (0.25×)

**Rationale:** This multiplier approach allows the application to handle various book formats while maintaining proportional cost relationships. The family-based organization ensures calculations remain accurate across different international paper standards.

## External Dependencies

### Python Packages

**Flask:**
- Purpose: Web framework for routing and template rendering
- Version: Not specified in repository (likely latest stable)
- Key features used: Route decorators, template rendering, request handling

**Math Module:**
- Purpose: Mathematical calculations for cost computations
- Standard library: No external installation required
- Usage: Likely for rounding and advanced calculations in the complete implementation

### Development Considerations

**Missing Components:**
The repository shows incomplete implementation:
- `main.py` is truncated (missing route implementation for `/calculate_multiple`)
- `attached_assets/main.py` appears to be a backup or alternate version
- Results template (`results.html`) is incomplete
- No requirements.txt or dependency specification file

**Runtime Environment:**
- No database required (stateless calculations)
- No authentication system needed
- Development: Flask development server (port 5000)
- Production: Gunicorn WSGI server for deployment

**Deployment Configuration:**
- Deployment type: Autoscale (pay-per-use)
- Production server: Gunicorn with `--reuse-port` flag
- Runs on port 5000, accessible globally
- Configured for worldwide access from any network (3G/4G/5G, WiFi)

### Currency Data

**Exchange Rate System:**
- Base currency: USD (rate: 1.0)
- Static exchange rates (not live API integration)
- Covers major global currencies with focus on Middle Eastern markets (AED, SAR, EGP)

**Note:** Exchange rates are hardcoded and will require manual updates. For production use, integration with a live currency API (e.g., Open Exchange Rates, Fixer.io) would be recommended.