from distutils.core import setup, Extension

def main():
    setup(name="trobot2",
          version="2.0.0",
          description="Python interface for the trobot C library function",
          author="thehomemadecode",
          author_email="thehomemadecode@gmail.com",
          ext_modules=[Extension("trobot2", ["trobot2module_work.c"])])

if __name__ == "__main__":
    main()
