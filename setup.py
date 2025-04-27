from setuptools import find_packages, setup 

setup( 
    name='dininghall-mealplan', 
    version='0.1', 
    description='', 
    author='', 
    author_email='', 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'flask-bcrypt',
        'flask-login',
        'Flask-WTF',
        'markupsafe',
        'pandas',
        'configparser',
        'pyotp',
        'Pillow',    
        'qrcode',
        'xlsxwriter',
        'WTForms-Alchemy',
        'email_validator'
    ]
) 