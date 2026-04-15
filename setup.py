from setuptools import find_packages, setup

setup(
    name="My_Project",
    version="0.0.1",
    author="Shubham Gupta",
    author_email="shubhamgupta43567@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pinecone-haystack",
        "haystack-ai",
        "fastapi",
        "uvicorn",
        "python-dotenv", 
        "langchain",
        "langchain-core",
        "langchain-community",
        "langchain-huggingface",
        
    ]
)