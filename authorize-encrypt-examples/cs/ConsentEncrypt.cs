using System;
using System.Security.Cryptography;
using System.Collections.Generic;
using Jose;


namespace Consent
{
    class ConsentEncrypt
    {

        static void Main(string[] args)
        {
            /*
                For the sake of simplicity, the JWK has been manually loaded into a dictionary.
                In "real life" you should process it from https://<ENV>.signicat.com/oidc/jwks.json
            */
            var jwk = new Dictionary<string, string>
            {
                {"kty", "RSA"},
                {"e", "AQAB"},
                {"use", "enc"},
                {"kid", "any.oidc-encryption-preprod.test.jwk.v.1"},
                {"alg", "RSA-OAEP"},
                {"n", "ou9ZQ_e0JSMhOA3fSwzH4h9OHgS8xLbtScHUlQEq9XWRw0i5ZefGWEUCeWJgehxuRMumPdm5_csfSnJLJom3c5cEnloXB53ZFEa6qJ7AEHnSjdMxnIkzcq_4ICQg69fwTac1ZCjxhCraUs6G9LE8b9gN-EHmd8MXuLRxZUkjlgiQKb-XhfDaDA7rd7KMczyxrieZT3q5lk1fjw2V_o_jasowLo8i7s8Wa4S7BAg1ZFv2-oc8PcobbJLsAAIxg3PEn0nDIvNcs6cjjYje2_TrrXMmis2TJquQhLOHjx_yQdzQNfzxC5_GwOZPBKZR1gH1-QxlW7q8jevC2-f_-7FlHw"}
            };

            // Preparing RSA key
            RSA key = RSA.Create();
            var rsaParam = new RSAParameters()
            {
                Modulus = Base64Url.Decode(jwk["n"]),
                Exponent = Base64Url.Decode(jwk["e"])
            };
            key.ImportParameters(rsaParam);

            // Token payload (JSON)
            var payload = new Dictionary<string, object>()
            {
                {"login_hint", new List<String>(){ "subject-198304062717" }},
                {"ui_locales", "sv"},
                {"scope", "openid profile signicat.sign"},
                {"signicat_signtext", "I confirm my purchase of broadband subscription Medium500."},
                {"acr_values", "urn:signicat:oidc:method:sbid-inapp-sign"},
                {"response_type", "code"},
                {"redirect_uri", "https://labs.signicat.com/redirect"},
                {"state", "ABCDEF012345"},
                {"client_id", "demo-inapp-sign"},
            };

            // Signicat OIDC server requires "kid" in header of JWE token
            var headers = new Dictionary<string, object>()
            {
                { "typ", "JWE"},
                { "kid", jwk["kid"]}
            };
            // Encoding JWE token
            string token = Jose.JWT.Encode(payload, key, JweAlgorithm.RSA_OAEP, JweEncryption.A256CBC_HS512, extraHeaders: headers);

            Console.WriteLine(token);
        }
    }
}
