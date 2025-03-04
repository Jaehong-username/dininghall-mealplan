# dininghall-mealplan

### Setup for development

Before you begin, ensure you have the following installed:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (version 3.8 or higher)

Before development, creating a python virtual environment is recommended.
To create a virtual environment, run:
````
python -m venv venv
````
then **activate the virtual environment** on Windows with:
````
.\venv\Scripts\Activate.ps1
````
or on Linux by running:
````
source ./venv/bin/activate
````
Then, **install all dependencies** with:
````
pip install -e .
````

### Running:
To run the **development server**, enter the ``src`` folder (``cd src``) and run:
````
python app.py
````

## Contributing:
1. Clone the repo: ``git clone https://github.com/Jaehong-username/dininghall-mealplan.git``
2. Checkout a new branch: ``git checkout -b branch-name``
3. Commit changes: ``git commit -am 'Commit name'``
4. Push to branch: ``git push origin branch-name``
5. Submit a pull request for that branch