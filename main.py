from website import create_app
# Website is a python package bc of the __init__.py -- so you can reference it :)

app = create_app()

# Only if we run this file-- not input, we will execute this line. 
# That way it runs when you run, and not while you import
if __name__ == '__main__':
    # everytime we make a change to python code, it will automatically rerun server
    # Turn off for production
   app.run(debug=True)
