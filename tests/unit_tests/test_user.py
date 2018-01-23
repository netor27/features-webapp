from unittest import TestCase

from web.models import User

class UsersTests(TestCase):

    def test_check_correct_password(self):
        name= "USER"
        password = "T3s!p4s5w0RDd12#"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertTrue(goodPassword, error)

    def test_check_correct_password_and_verify_the_hash(self):
        name= "USER"
        password = "T3s!p4s5w0RDd12#"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertTrue(goodPassword, error)
        password_verified = user.verify_password(password)
        self.assertTrue(password_verified, "The password could not be verified")
    
    def test_incorrect_password_too_short(self):
        name= "USER"
        password = "a"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password is too short')

    def test_incorrect_password_too_long(self):
        name= "USER"
        password = "a"*50
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password is too long')


    def test_incorrect_password_without_uppercase_letter(self):
        name= "USER"
        password = "t3s!p4s5w0rd12#"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password must include at least one uppercase letter')

    def test_incorrect_password_without_lowercase_letter(self):
        name= "USER"
        password = "T3S!P4S5W0RD12#"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password must include at least one lowercase letter')
    
    def test_incorrect_password_without_number(self):
        name= "USER"
        password = "TeS!PaSsWoRDds#"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password must include at least one number')

    def test_incorrect_password_without_symbol(self):
        name= "USER"
        password = "TeS41PaSsWoRDds"
        user = User(name)
        error, goodPassword = user.check_password_strength_and_hash_if_ok(password)
        self.assertFalse(goodPassword)
        self.assertEqual(error, 'The password must include at least one symbol')