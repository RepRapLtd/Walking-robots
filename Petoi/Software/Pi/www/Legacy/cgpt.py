# Import the Flask library
from flask import Flask, render_template, request

# Create a new Flask app
app = Flask(__name__)

# Define a route to display the home page
@app.route('/')
def home():
  # Render the home page template
  return render_template('home.html')

# Define a route to handle adding items to the list
@app.route('/add-item', methods=['POST'])
def add_item():
  # Get the item value from the POST request
  item = request.form['item']

  # Add the item to the list
  items.append(item)

  # Redirect the user back to the home page
  return redirect('/')

# Define a route to handle deleting items from the list
@app.route('/delete-item/<item>')
def delete_item(item):
  # Remove the item from the list
  items.remove(item)

  # Redirect the user back to the home page
  return redirect('/')

# Define a global list to hold the items
items = []

# Run the app when the script is executed
if __name__ == '__main__':
  app.run()

