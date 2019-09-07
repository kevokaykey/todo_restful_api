""" Test user module """
import unittest

Class TestUser():

def test_valid_login_generates_token(self):
        """Tests token is generated on successful login."""
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(self.user),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("token", response_msg)

if __name__ =="__main__":
    unittest.main()        