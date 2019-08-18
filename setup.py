from distutils.core import setup
import setuptools

setup(
  name = "Logen",
  packages = ["Logen"],
  entry_points = {
      "console_scripts": ["logen = Logen:main"]
  },
  version = "0.1.1",
  license = "MIT",
  description = "Generates and converts between various localization formats.",
  long_description = "Generates and converts between various localization formats.",
  author = "David Piper",
  author_email = "david@dpiper.de",
  url = "https://github.com/DavidPiper94",     # Provide either the link to your github or to your website
  download_url = "https://github.com/DavidPiper94/Logen/archive/v_0.1.1.tar.gz",
  keywords = [
      "localization",
      "converter",
      "ios",
      "android",
    ],
  classifiers = [
    "Development Status :: 3 - Alpha",          # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    "Intended Audience :: Developers",          # Define that your audience are developers
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",      # Specify which pyhton versions that you want to support
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)