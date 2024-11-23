import random
import string

import jwt
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test randomly generated JWT_SECRET values for compatibility during encoding and decoding"

    def handle(self, *args, **kwargs):
        JWT_ALGORITHM = "HS256"
        payload = {"data": "test"}
        failed_secrets = []

        def generate_random_secret():
            # Generate a random secret with variable lengths and characters
            length = random.randint(10, 64)  # Random length between 10 and 64
            chars = (
                string.ascii_letters + string.digits + string.punctuation
            )  # Include special characters
            return "".join(random.choices(chars, k=length))

        for i in range(5000000):
            jwt_secret = generate_random_secret()

            try:
                # Test encoding and decoding
                encoded_token = jwt.encode(payload, jwt_secret, algorithm=JWT_ALGORITHM)
                decoded_payload = jwt.decode(
                    encoded_token, jwt_secret, algorithms=[JWT_ALGORITHM]
                )
            except Exception as e:
                # Capture failing secrets
                failed_secrets.append((jwt_secret, str(e)))

        # Print results
        if failed_secrets:
            self.stdout.write(self.style.ERROR("Failed JWT_SECRETs:"))
            for secret, error in failed_secrets:
                self.stdout.write(f"Secret: {secret} | Error: {error}")
        else:
            self.stdout.write(self.style.SUCCESS("All JWT_SECRETs worked correctly!"))
