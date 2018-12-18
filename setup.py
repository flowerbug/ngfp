#
#
# Copyright 2018 Ant <ant@anthive.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ngfp",
    version="0.1.5",
    author="Ant",
    author_email="ant@anthive.com",
    description="A puzzle game based upon gfpoken.",
    long_description=long_description,
    url="https://salsa.debian.org/ant-guest/gfpoken-in-python",
    packages=setuptools.find_packages(),
    install_requires=["pyglet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Games/Entertainment :: Puzzle Games"
    ],
    python_requires='>=3'
)
