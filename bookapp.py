from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Dropdown options
paper_sizes = [
    "0.57 x 0.82",
    "0.70 x 1.00",
    "0.60 x 0.90"
]
cover_types = [
    {"type": "مجلد", "price_range": [0.5, 1.0, 1.5]},
    {"type": "سحاب", "price_range": [0.75, 1.25, 1.5]},
    {"type": "كرتونية", "price_range": [1.0, 1.5, 2.0]},
    {"type": "فني", "price_range": [1.25, 1.5, 2.5]},
]

@app.route('/')
def index():
    return render_template('index.html', paper_sizes=paper_sizes, cover_types=cover_types)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Single book calculation logic
        num_pages = int(request.form['num_pages'])
        paper_size = request.form['paper_size']
        paper_weight_per_m2 = float(request.form['paper_weight_per_m2'])
        num_books = int(request.form['num_books'])
        num_colors = int(request.form['num_colors'])
        cover_type = request.form['cover_type']
        cover_price = float(request.form['cover_price'])
        profit_margin = float(request.form['profit_margin'])
        paper_price_per_ton = float(request.form['paper_price_per_ton'])
        waste = int(request.form['waste'])
        num_moujalad = int(request.form['num_moujalad'])

        print(f"Number of Moujalads: {num_moujalad}")


        paper_length, paper_width = map(float, paper_size.split(' x '))

        # Fixed costs
        printing_cost_per_10k = 10
        folding_cost_per_1k = 2
        plate_cost = 10
        shipping_cost_per_kg = 0.1

        # Calculations
        num_booklets = math.ceil(num_pages / 16)
        paper_weight_per_booklet = paper_length * paper_width * 500 * paper_weight_per_m2
        paper_cost = num_booklets * (num_books + waste) * paper_weight_per_booklet * (paper_price_per_ton / 1000)
        printing_cost = num_booklets * num_colors * printing_cost_per_10k
        folding_cost = (num_booklets * num_books / 1000) * folding_cost_per_1k
        plate_cost_total = num_booklets * num_colors * plate_cost
        shipping_cost = (num_books / 1000) * paper_weight_per_booklet * num_booklets * shipping_cost_per_kg

        total_cost_without_cover = (paper_cost + printing_cost + folding_cost + plate_cost_total + shipping_cost) / num_books
        total_cost_with_cover = total_cost_without_cover + (cover_price * num_moujalad)
        final_book_price = total_cost_with_cover * (1 + profit_margin / 100)

        total_cost_without_cover = round(total_cost_without_cover, 2)
        total_cost_with_cover = round(total_cost_with_cover, 2)
        final_book_price = round(final_book_price, 2)

        return render_template(
            'results.html',
            num_booklets=num_booklets,
            paper_weight_per_booklet=round(paper_weight_per_booklet, 2),
            paper_cost=round(paper_cost, 2),
            printing_cost=round(printing_cost, 2),
            folding_cost=round(folding_cost, 2),
            plate_cost_total=round(plate_cost_total, 2),
            shipping_cost=round(shipping_cost, 2),
            total_cost_without_cover=total_cost_without_cover,
            total_cost_with_cover=total_cost_with_cover,
            cover_type=cover_type,
            final_book_price=final_book_price
        )
    except Exception as e:
        return f"An error occurred: {e}"

# Add the `calculate_multiple` function below `calculate`
@app.route('/calculate_multiple', methods=['POST'])
def calculate_multiple():
    try:
        # Get list of books from the form
        books = request.form.to_dict(flat=False)
        results = []

        for i in range(len(books['books[][num_pages]'])):
            # Extract book-specific inputs
            num_pages = int(books['books[][num_pages]'][i])
            paper_size = books['books[][paper_size]'][i]
            paper_weight_per_m2 = float(books['books[][paper_weight_per_m2]'][i])
            num_books = int(books['books[][num_books]'][i])
            num_colors = int(books['books[][num_colors]'][i])
            cover_type = books['books[][cover_type]'][i]
            cover_price = float(books['books[][cover_price]'][i])
            profit_margin = float(books['books[][profit_margin]'][i])
            paper_price_per_ton = float(books['books[][paper_price_per_ton]'][i])
            waste = int(books['books[][waste]'][i])
            num_moujalad = int(books['books[][num_moujalad]'][i])

            # Reuse single book calculation logic
            num_booklets = math.ceil(num_pages / 16)
            paper_length, paper_width = map(float, paper_size.split(' x '))
            paper_weight_per_booklet = paper_length * paper_width * 500 * paper_weight_per_m2
            paper_cost = (num_booklets * (num_books + waste) * paper_weight_per_booklet * paper_price_per_ton) / 1000
            printing_cost = num_booklets * num_colors * 10
            folding_cost = num_booklets * num_books / 1000 * 2
            plate_cost_total = num_booklets * num_colors * 10
            shipping_cost = num_books / 1000 * paper_weight_per_booklet * num_booklets * 0.1
            total_cost_without_cover = (paper_cost + printing_cost + folding_cost + plate_cost_total + shipping_cost) / num_books
            total_cost_with_cover = total_cost_without_cover + (cover_price * num_moujalad)
            final_book_price = total_cost_with_cover * (1 + profit_margin / 100)
         
            results.append({
             'num_pages': num_pages,
              'num_books': num_books,
              'num_booklets': num_booklets,
            'paper_length': paper_length,
            'paper_width': paper_width,
            'paper_weight_per_booklet': round(paper_weight_per_booklet, 2),
            'paper_cost': round(paper_cost, 2),
            'printing_cost': round(printing_cost, 2),
          'folding_cost': round(folding_cost, 2),
          'plate_cost_total': round(plate_cost_total, 2),
          'shipping_cost': round(shipping_cost, 2),
          'total_cost_without_cover': round(total_cost_without_cover, 2),
          'total_cost_with_cover': round(total_cost_with_cover, 2),
          'num_moujalad': num_moujalad,
          'final_book_price': round(final_book_price, 2)
})


        return render_template('results.html', results=results)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

