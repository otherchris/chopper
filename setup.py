import setuptools

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Parse dependencies from requirements.txt
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="chopper",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI for recording or chopping audio snippets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        "cli",
        "audio_devices",
        "play_audio",
        "record_snippets",
    ],
    entry_points={
        'console_scripts': [
            'chopper=cli:main',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
