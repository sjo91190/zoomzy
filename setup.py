from setuptools import setup, find_packages

setup(
    name="zoomzy",
    version="1.0.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["click==7.1.2", "Flask==1.1.2", "Flask-WTF==0.14.3",
                      "itsdangerous==1.1.0", "Jinja2==2.11.2", "MarkupSafe==1.1.1",
                      "Paste==3.5.0", "Pillow==8.0.1", "six==1.15.0", "waitress==1.4.4",
                      "Werkzeug==1.0.1", "WTForms==2.3.3"],
    author="Sam O'Keefe",
    author_email="sjo91190@gmail.com",
    description="Some games to play on a zoom party",
    url="https://github.com/sjo91190/zoomzy"
)
