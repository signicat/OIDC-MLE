const jose = require('node-jose');
let key;
let enc;

/*
    For the sake of simplicity, the JWK has been manually loaded into a JSON.
    In "real life" you should process it from https://<ENV>.signicat.com/oidc/jwks.json
*/
jwk = {
    "kty": "RSA",
    "e": "AQAB",
    "use": "enc",
    "kid": "any.oidc-encryption-preprod.test.jwk.v.1",
    "alg": "RSA-OAEP",
    "n": "ou9ZQ_e0JSMhOA3fSwzH4h9OHgS8xLbtScHUlQEq9XWRw0i5ZefGWEUCeWJgehxuRMumPdm5_csfSnJLJom3c5cEnloXB53ZFEa6qJ7AEHnSjdMxnIkzcq_4ICQg69fwTac1ZCjxhCraUs6G9LE8b9gN-EHmd8MXuLRxZUkjlgiQKb-XhfDaDA7rd7KMczyxrieZT3q5lk1fjw2V_o_jasowLo8i7s8Wa4S7BAg1ZFv2-oc8PcobbJLsAAIxg3PEn0nDIvNcs6cjjYje2_TrrXMmis2TJquQhLOHjx_yQdzQNfzxC5_GwOZPBKZR1gH1-QxlW7q8jevC2-f_-7FlHw"
}

// Token payload (JSON)
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
const payload_buffer = Buffer.from(JSON.stringify(payload));

// Preparing RSA key
jose.JWK.asKey(jwk).then((result) => {
    key = result;
    
    // Encoding JWE token
    // Signicat OIDC server requires "kid" in header of JWE token (node-jose does it automatically)
    jose.JWE.createEncrypt({ format: 'compact' }, key).update(payload_buffer).final().then((result) => {
        enc = result;
        console.log(enc);
    }, (error) => {
        console.log("ERROR: ", error.message);
    });
}, (error) => {
    console.log("ERROR: ", error.message);
});