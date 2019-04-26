# Functional Example of "Full Message-Level Encryption" for FTN

---

This shows how to perform an OIDC flow with Full Message-Level Encryption, as specified in the requirements for FTN (Finnish Trust Network).

## Instructions

* First you need to generate a JWK RSA pair (2048 or 4096-bit).
* It’s important that you create an JWK and not a PEM, CER, CRT etc. 
  * Send the public part to Signicat (The public part can be sent through email as its not sensitive)

### Customer implementation

Begin crafting the OIDC Authorization Request. The parameters are standard OIDC parameters, but the payload has to be encrypted for security, to ensure the integrity of the signature. The requirements are as follows:

* The HTTP request can be made using either GET or POST.
* The payload must be a Request Object (per OIDC Core specifications, section 6.1). 
* The request must be an encrypted JWT, which contains the aforementioned Request Object (as specified at https://openid.net/specs/openid-connect-core-1_0.html#JWTRequests).
* The JWE token must be encrypted with the public key ("use":"enc") available at https://<ENV>.signicat.com/oidc/jwks.json.
* The protected header for the JWE token must contain the following claims:
  * "enc"="A256CBC-HS512"
  * "typ"="JWE"
  * "kid" and "alg" (the values for “kid” and “alg” are specified at https://<ENV>.signicat.com/oidc/jwks.json).

The ID token and the response from user info is a nested JWT, that is encrypted and signed.

1. Decrypt it with your private from the RSA pair given to Signicat. 
2. Deserialize the resulting signed JWT and verify the signature. 

The ID-token must be, as always, verified according OIDC specifications. To able to read the response from user info follow the process above. 

* Encrypted with key provided by customer.
* Signed with key from https://<ENV>.signicat.com/oidc/jwks.json ("use": "sig")

ENV = preprod.signicat.com for test and id.signicat.com for production.

## Usage

Recommended to use pipenv.

`pipenv install` & `pipenv run python ftn-mle-example.py` to run it.
