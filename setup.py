from distutils.core import setup, Extension

def main():
    setup(name="trobot",
          version="1.0.0",
          description="Python interface for the sum C library function",
          author="<your name>",
          author_email="your_email@gmail.com",
          ext_modules=[Extension("trobot", ["test.c"])])

if __name__ == "__main__":
    main()
