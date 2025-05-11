from setuptools import setup, find_packages


setup(
    name='Dabas',
    version='1.0.2',
    author='Abbas Bachari',
    author_email='abbas-bachari@hotmail.com',
    description="A Python library for Database Management",
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/abbas-bachari/Dabas',
    python_requires='>=3.8',
    project_urls={
    "Homepage":'https://github.com/abbas-bachari/Dabas',
    'Documentation': 'https://github.com/abbas-bachari/Dabas',
    'Source': 'https://github.com/abbas-bachari/Dabas/',
    'Tracker': 'https://github.com/abbas-bachari/Dabas/issues',
   
},
    
    install_requires=['SQLAlchemy >= 1.4'],
    keywords=['Dabas',  'Database', 'Database-Management', 'Dabas-python', 'SQLAlchemy', 'SQLAlchemy-python', 'Dabas-SQLAlchemy', 'Dabas-SQLAlchemy-python', 'SQLAlchemy-Database-Management'],
    classifiers=[
        'Intended Audience :: Developers',
        "Intended Audience :: Financial and Insurance Industry",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        
        
    ],
    
    
)

