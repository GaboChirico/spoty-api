from setuptools import setup

setup(
    name="spoty",
    version="0.2.0",
    description="Spotify API",
    packages=".src/spoty/api",
    install_requires=[
        "spotipy==2.20.0",
        "pandas==1.5.0",
    ],
    python_requires=">=3.10",
)

if __name__ == "__main__":
    setup()
