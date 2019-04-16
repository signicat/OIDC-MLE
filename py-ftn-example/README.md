# Functional Example of "Full Message-Level Encryption" for FTN

---

This shows how to perform an OIDC flow with Full Message-Level Encryption, as specified in the requirements for FTN (Finnish Trust Network).

There are three steps to the process:

1. Generate a RSA-pair (2048 or 4096-bit), stored as a JWK. Send the **public part** to Signicat so that we can configure your service. Signicat will use it to encrypt our responses.
2. Encrypt your request to /authorize end-point.
3. Decrypt the responses sent by Signicat OIDC server.

## Usage

Recommended to use pipenv.

`pipenv install` & `pipenv run python ftn-mle-example.py` to run it.
