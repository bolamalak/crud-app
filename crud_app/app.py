from flask import Flask, render_template, request, redirect, flash
import pymysql

app = Flask(__name__)
app.secret_key = "your_secret_key"


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Bola@2040",
    database="crud_app"
)

@app.route("/")
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template("index.html", products=products)
@app.route("/add", methods=["POST"])
def add_product():
    try:
        name = request.form["name"]
        price = request.form["price"]

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            (name, price)
        )

        connection.commit()
        flash("Product added successfully!")

        return redirect("/")

    except Exception:
        flash("Error adding product!")
        return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()

        if product is None:
            flash("Product not found!")
            return redirect("/")

        if request.method == "POST":
            name = request.form["name"]
            price = request.form["price"]

            cursor.execute(
                "UPDATE products SET name = %s, price = %s WHERE id = %s",
                (name, price, id)
            )

            connection.commit()
            flash("Product updated successfully!")

            return redirect("/")

        return render_template("edit.html", product=product)

    except Exception:
        flash("Error updating product!")
        return redirect("/")

@app.route("/delete/<int:id>")
def delete_product(id):
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM products WHERE id = %s",
            (id,)
        )

        connection.commit()
        flash("Product deleted successfully!")

        return redirect("/")

    except Exception:
        flash("Error deleting product!")
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)