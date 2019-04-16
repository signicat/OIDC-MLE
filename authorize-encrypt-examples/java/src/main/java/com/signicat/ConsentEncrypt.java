
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.signicat;

import java.util.*;
import com.nimbusds.jose.*;
import com.nimbusds.jose.crypto.*;
import com.nimbusds.jose.jwk.*;
import net.minidev.json.*;
import java.text.ParseException;


/**
 *
 * @author dag
 */
public class ConsentEncrypt {
    
    public static void main(String[] args) throws ParseException, JOSEException{
        
        /*
            For the sake of simplicity, the JWK has been manually loaded into a String.
            In "real life" you should process it from https://<ENV>.signicat.com/oidc/jwks.json
        */
        String jwk = "{ \"kty\": \"RSA\", \"e\": \"AQAB\", \"use\": \"enc\", \"kid\": \"any.oidc-encryption-preprod.test.jwk.v.1\", \"alg\": \"RSA-OAEP\", \"n\": \"ou9ZQ_e0JSMhOA3fSwzH4h9OHgS8xLbtScHUlQEq9XWRw0i5ZefGWEUCeWJgehxuRMumPdm5_csfSnJLJom3c5cEnloXB53ZFEa6qJ7AEHnSjdMxnIkzcq_4ICQg69fwTac1ZCjxhCraUs6G9LE8b9gN-EHmd8MXuLRxZUkjlgiQKb-XhfDaDA7rd7KMczyxrieZT3q5lk1fjw2V_o_jasowLo8i7s8Wa4S7BAg1ZFv2-oc8PcobbJLsAAIxg3PEn0nDIvNcs6cjjYje2_TrrXMmis2TJquQhLOHjx_yQdzQNfzxC5_GwOZPBKZR1gH1-QxlW7q8jevC2-f_-7FlHw\" }";
        RSAKey jwkey = RSAKey.parse(jwk);
        
        // Token payload (JSON)
        JSONObject payload_json = new JSONObject();
        List<String> login_hint = new ArrayList<>();
        login_hint.add("subject-198304062717");
        payload_json.put("login_hint", login_hint);
        payload_json.put("ui_locales", "sv");
        payload_json.put("scope", "openid profile signicat.sign");
        payload_json.put("signicat_signtext", "I confirm my purchase of broadband subscription Medium500.");
        payload_json.put("acr_values", "urn:signicat:oidc:method:sbid-inapp-sign");
        payload_json.put("response_type", "code");
        payload_json.put("redirect_uri", "https://labs.signicat.com/redirect");
        payload_json.put("state", "ABCDEF012345");
        payload_json.put("client_id", "demo-inapp-sign");
        Payload payload = new Payload(payload_json);
        
        // Signicat OIDC server requires "kid" in header of JWE token
        JWEHeader header = new JWEHeader.Builder(JWEAlgorithm.RSA_OAEP, EncryptionMethod.A256CBC_HS512).keyID("any.oidc-encryption-preprod.test.jwk.v.1").build();
        
        // Create a JWEObject with header and JSON payload
        JWEObject jweObject = new JWEObject(header, payload);
        
        // Create an encrypter with the specified public RSA key
        RSAEncrypter encrypter = new RSAEncrypter(jwkey.toPublicJWK());
        
        // // Encoding JWE token
        jweObject.encrypt(encrypter);

        System.out.println(jweObject.serialize());
    }
    
}
