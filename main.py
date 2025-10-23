from flask import Flask, render_template, request
import math

app = Flask(__name__, template_folder='bookcalculation')

# Reference sheet dropdown options
paper_sizes = ["0.57 x 0.82", "0.60 x 0.90", "0.70 x 1.00"]

# Define final (trimmed) size multipliers for each family
# e.g., "35 x 25" => ×2, "50 x 35" => ×4, "12 x 17" => ÷2, etc.
final_size_multipliers = {
    # 70×100 family
    "17 x 24": 1.0,  # standard
    "35 x 25": 2.0,  # 1 step above
    "50 x 35": 4.0,  # 2 steps above
    "12 x 17": 0.5,  # 1 step below
    "8 x 12": 0.25,  # 2 steps below
    "6 x 8": 0.25,  # 2 steps below (or more)

    # 82×57 family
    "14 x 20": 1.0,
    "20 x 28": 2.0,
    "40 x 28": 4.0,
    "10 x 14": 0.5,
    "7 x 10": 0.25,

    # 90×60 family
    "15 x 22": 1.0,
    "30 x 22.5": 2.0,
    "45 x 30": 4.0,
    "11.5 x 15": 0.5,
    "7.5 x 11": 0.25
}

# Currency exchange rates
currency_rates = {
    'USD': {
        'symbol': '$',
        'rate': 1.0,
        'name': 'US Dollar'
    },
    'EUR': {
        'symbol': '€',
        'rate': 0.92,
        'name': 'Euro'
    },
    'GBP': {
        'symbol': '£',
        'rate': 0.79,
        'name': 'British Pound'
    },
    'AED': {
        'symbol': 'د.إ',
        'rate': 3.67,
        'name': 'UAE Dirham'
    },
    'SAR': {
        'symbol': 'ر.س',
        'rate': 3.75,
        'name': 'Saudi Riyal'
    },
    'EGP': {
        'symbol': 'ج.م',
        'rate': 30.90,
        'name': 'Egyptian Pound'
    },
    'JPY': {
        'symbol': '¥',
        'rate': 149.50,
        'name': 'Japanese Yen'
    },
    'CNY': {
        'symbol': '¥',
        'rate': 7.24,
        'name': 'Chinese Yuan'
    },
    'INR': {
        'symbol': '₹',
        'rate': 83.12,
        'name': 'Indian Rupee'
    },
    'TRY': {
        'symbol': '₺',
        'rate': 28.50,
        'name': 'Turkish Lira'
    }
}

# Regional shipping costs (per kg)
regional_shipping = {
    'Local': {
        'name_ar': 'محلي',
        'cost_per_kg': 0.1
    },
    'Middle East': {
        'name_ar': 'الشرق الأوسط',
        'cost_per_kg': 0.5
    },
    'North Africa': {
        'name_ar': 'شمال أفريقيا',
        'cost_per_kg': 0.6
    },
    'Europe': {
        'name_ar': 'أوروبا',
        'cost_per_kg': 1.0
    },
    'Asia': {
        'name_ar': 'آسيا',
        'cost_per_kg': 1.2
    },
    'North America': {
        'name_ar': 'أمريكا الشمالية',
        'cost_per_kg': 1.5
    },
    'South America': {
        'name_ar': 'أمريكا الجنوبية',
        'cost_per_kg': 1.8
    },
    'Africa': {
        'name_ar': 'أفريقيا',
        'cost_per_kg': 1.3
    },
    'Oceania': {
        'name_ar': 'أوقيانوسيا',
        'cost_per_kg': 2.0
    }
}


@app.route('/')
def index():
    """
    Renders an HTML form that lets the user add multiple books,
    each with a reference paper size and a final trimmed size.
    """
    return render_template('index.html',
                           paper_sizes=paper_sizes,
                           currencies=currency_rates,
                           regions=regional_shipping)


@app.route('/calculate_multiple', methods=['POST'])
def calculate_multiple():
    try:
        # Retrieve all form data
        books = request.form.to_dict(flat=False)
        results = []

        # How many books were submitted?
        num_items = len(books['books[][num_pages]'])

        for i in range(num_items):
            # 1. Extract fields for each book
            num_pages = int(books['books[][num_pages]'][i])
            reference_paper_size = books['books[][paper_size]'][i]
            final_book_size = books['books[][final_book_size]'][i]
            paper_weight_per_m2 = float(
                books['books[][paper_weight_per_m2]'][i])
            num_books = int(books['books[][num_books]'][i])
            num_colors = int(books['books[][num_colors]'][i])
            cover_price = float(books['books[][cover_price]'][i])
            profit_margin = float(books['books[][profit_margin]'][i])
            paper_price_per_ton = float(
                books['books[][paper_price_per_ton]'][i])
            waste = int(books['books[][waste]'][i])
            num_moujalad = int(books['books[][num_moujalad]'][i])

            # 2. Constants
            printing_cost_per_10k = 6
            folding_cost_per_1k = 2
            plate_cost_unit = 10
            shipping_cost_per_kg = 2

            # 3. Calculate number of booklets (each 16 pages)
            num_booklets = math.ceil(num_pages / 16)

            # 4. Calculate paper weight per booklet
            paper_length, paper_width = map(float,
                                            reference_paper_size.split(' x '))
            paper_weight_per_booklet = paper_length * paper_width * 500 * paper_weight_per_m2

            # 5. Base cost calculations (before multiplier)
            paper_cost = (num_booklets *
                          (num_books + waste) * paper_weight_per_booklet *
                          paper_price_per_ton) / 1000

            printing_cost = num_booklets * num_colors * printing_cost_per_10k
            folding_cost = (num_booklets * num_books /
                            1000) * folding_cost_per_1k
            plate_cost_total = num_booklets * num_colors * plate_cost_unit
            shipping_cost = ((num_books / 1000) * paper_weight_per_booklet *
                             num_booklets * shipping_cost_per_kg)

            # 6. Apply final size multiplier to paper, printing, plates
            size_multiplier = final_size_multipliers.get(final_book_size, 1.0)
            paper_cost *= size_multiplier
            printing_cost *= size_multiplier
            plate_cost_total *= size_multiplier
            # folding_cost & shipping_cost remain unchanged

            # 7. Summation + per-book cost
            total_cost_without_cover = (paper_cost + printing_cost +
                                        folding_cost + plate_cost_total +
                                        shipping_cost) / num_books

            # 8. Add cover cost
            total_cost_with_cover = total_cost_without_cover + (cover_price *
                                                                num_moujalad)

            # 9. Profit margin
            final_book_price = total_cost_with_cover * (1 +
                                                        profit_margin / 100)

            # 10. Store results for this book
            results.append({
                'num_pages':
                num_pages,
                'reference_paper_size':
                reference_paper_size,
                'final_book_size':
                final_book_size,
                'num_booklets':
                num_booklets,
                'paper_weight_per_booklet':
                round(paper_weight_per_booklet, 2),
                'paper_cost':
                round(paper_cost, 2),
                'printing_cost':
                round(printing_cost, 2),
                'folding_cost':
                round(folding_cost, 2),
                'plate_cost_total':
                round(plate_cost_total, 2),
                'shipping_cost':
                round(shipping_cost, 2),
                'total_cost_without_cover':
                round(total_cost_without_cover, 2),
                'total_cost_with_cover':
                round(total_cost_with_cover, 2),
                'cover_price':
                round(cover_price, 2),
                'profit_margin':
                profit_margin,
                'num_moujalad':
                num_moujalad,
                'final_book_price':
                round(final_book_price, 2)
            })

        # Render a table of results
        return render_template('results.html', results=results)

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
