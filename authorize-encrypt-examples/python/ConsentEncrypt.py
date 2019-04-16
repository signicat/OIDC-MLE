import json
import random
from jwcrypto import jwk, jwe


# For the sake of simplicity, the JWK has been manually loaded into a dictionary.
# In "real life" you should process it from https://<ENV>.signicat.com/oidc/jwks.json
jwkey = {
    "kty": "RSA",
    "e": "AQAB",
    "use": "enc",
    "kid": "any.oidc-encryption-preprod.test.jwk.v.1",
    "alg": "RSA-OAEP",
    "n": "ou9ZQ_e0JSMhOA3fSwzH4h9OHgS8xLbtScHUlQEq9XWRw0i5ZefGWEUCeWJgehxuRMumPdm5_csfSnJLJom3c5cEnloXB53ZFEa6qJ7AEHnSjdMxnIkzcq_4ICQg69fwTac1ZCjxhCraUs6G9LE8b9gN-EHmd8MXuLRxZUkjlgiQKb-XhfDaDA7rd7KMczyxrieZT3q5lk1fjw2V_o_jasowLo8i7s8Wa4S7BAg1ZFv2-oc8PcobbJLsAAIxg3PEn0nDIvNcs6cjjYje2_TrrXMmis2TJquQhLOHjx_yQdzQNfzxC5_GwOZPBKZR1gH1-QxlW7q8jevC2-f_-7FlHw"
}

# Preparing RSA key
rsakey = jwk.JWK()
rsakey.import_key(**jwkey)

# Token payload (JSON)
payload = {
    "login_hint": ["subject-198304062717"],
    "ui_locales": "sv",
    "scope": "openid profile signicat.sign",
    "signicat_signtext": "I confirm my purchase of broadband subscription Medium500.",
    "acr_values": "urn:signicat:oidc:method:sbid-inapp-sign",
    "response_type": "code",
    "redirect_uri": "https://labs.signicat.com/redirect",
    "state": "ABCDEF012345",
    "client_id": "demo-inapp-sign",
}
payload_bytes = json.dumps(payload).encode('utf-8')

# Signicat OIDC server requires "kid" in header of JWE token
header = {
    "alg": jwkey["alg"],
    "enc": "A256CBC-HS512",
    "typ": "JWE",
    "kid": jwkey["kid"],
}
# Encoding JWE token
jwetoken = jwe.JWE(payload_bytes, recipient=rsakey, protected=header)
enc = jwetoken.serialize(compact=True)

print(enc)