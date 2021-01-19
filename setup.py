import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="articutapi",
    version="1.0.2",
    author="Droidtown Linguistic Tech. Co. Ltd.",
    author_email="info@droidtown.co",
    description="Articut NLP system provides not only finest results on Chinese word segmentaion (CWS), Part-of-Speech tagging (POS) and Named Entity Recogintion tagging (NER), but also the fastest online API service in the NLP industry.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Droidtown/ArticutAPI",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["requests >= 2.25.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.1',
)

