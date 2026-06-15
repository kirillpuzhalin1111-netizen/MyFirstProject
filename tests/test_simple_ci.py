"""Простые тесты для CI/CD"""
import sys
import os

class TestSimple:
    def test_addition(self):
        assert 1 + 1 == 2
    
    def test_subtraction(self):
        assert 5 - 3 == 2
    
    def test_string_upper(self):
        assert "hello".upper() == "HELLO"
    
    def test_list_length(self):
        assert len([1, 2, 3]) == 3
