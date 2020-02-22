#!flask/bin/python
# coding=utf-8

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

if __name__ == '__main__':
    a = 'aaaa'
    b = a
    b = 'bbbb'
    print(a, b)
