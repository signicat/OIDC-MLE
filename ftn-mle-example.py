import requests
import json
from jwcrypto import jwk, jwe, jws

# jwk_full is the RSA key-pair which Signicat's OIDC server will use to encrypt the ID token and UserInfo responses. Signicat has only the public part.
# You (our customer) need the full pair, as you need the private key to decrypt the responses.
# This RSA key-pair can be generated in many ways. For this example is it generated using: https://jwcrypto.readthedocs.io/en/latest/jwk.html#examples
'''
jwk = jwk.JWK.generate(kty='RSA', size=4096)    - generates the RSA key-pair
jwk.export()                                    - exports the full key-pair
jwk.export(private_key=False)                   - exports ONLY the public part.
'''
# This RSA private key has to be considered highly sensitive data, it must be stored in a very secure location. 
jwk_full = { "d": "Na7lzZR8gTmiJjOnrSew49tT8Qxl7-wFEJAk8_IAKmS1KidtNrNxt5GgBsy7Uksk0EXwYmbxLY7ke_yvGNtDTAaR71VWJyTDYJjiu-D-cMrRWGxLUtf0SDQtuf5_7rVNikmuUgxtaNZowstBZog-W8QIpGv7nvfOKchFK-Cf92ApWWU6DH3vN60TQtk9f8e_XLM4Yy2iBEghU58VNegb8mS9Bg-WfiG8Bf8opjj2IxlssqK98AlXPIZ-T-Xar6D9SkOVYTuracOoxSQjOEKHVCtluGQRinP3yxAQvF81ZPp2zO7LbSx2NRB4h2DzcUXSnMbY2PXgw4Sqs7QlJ7miKgrFyseRgikzZNDLv-8jhujkjRfAZ3VZFPy5-LKtG1uLf8erwwLedCqg9ClTLiXMG05uogdXIB8hYjP04ZWPNR_hQwKAEo3yFsS0SSMBOO4ANjc_uzQf7xmnKei0imDfJcufMFCvPuT_F4x6xJzi_DSLOW8s7KDFvFBTBgnTsoVHIAWDXGXM9iebLx26NwgtUcclfm2hidcsuJnS4Qyx9r-AHjxNH7uVNZP3eyjXqH4jrmweLzOGpSuLIGiXfAi7aVFISH5dD4eaq-zkxZgV-Vs8iRD8TlhYb7ETYxM71fw3Ga-rp9hAHY2_pHz3iCs3yIL08u6CGqe6udB10WmTdjk", "dp": "VYi8AKFAbw0yu5xZcf8MKwQwVSCIqZyw7gZDaz5Exz00XKHVWKlUdvqQH52e9GYW84rqdhCINcXctEnT9kfrUJRp6sg40aFWSfZNGvN0ZlwgHsuk8BKXdD0k8evgEH4iomHk5V6b8Au8ilJN3JlI3mW7ZM4aHqODfPXoNAAwHXNX24hnX3on3Y9xZvEoGZKn4WnU7rGZjcsIYphy3IGfIe0BlZYGTHnteAFjsK0ODXoGXSh2ZvhiDKO6fl57lS_h43i5gLsIOtM-T9uGFFe681h4OcM3HQNcYnwvl0RpdKXIKhVn54w7yKc1e3x6bEO5nj0ZPFwAbLWDZ0ljv_SpOw", "dq": "cqloF7Ips92f75WR2xHAuM7GmpywEWZjdiwbHqDQ79cLFbfQxO99J9kpC9kjTRE4T21OdpHOBtEIQYF8mroEHNtI9guBR1sQwMxx_DHyyJ0M1HHrzBawQr9DqqmqfHNkPCLetwv2E0sOd90CvUU6zL9p0f-Npn4-l1r7KsSAn2w5oDy4fb0ZAn4Lc4GtISYNV9SX9rpZN83WlF1oOzOWenTwiWrQneicRdM5L7HxWBs-FQQX5oi32xSf3chwy9o2po2DUD3Ess5BH-Y0lmDH6hEufwHbKRpKzWLxhZwa0BkbFL68ypbeWK-dUNdh5HCCNup0IpCgP1-_6PnQU-vw9Q", "e": "AQAB", "kty": "RSA", "n": "psPFRnGgt4wJK--20KG0M_AgL2B-J0Q4Nrd3duq0lt2kXwtD5MdAmpWpPncQgMzqVT3IyuEjFjHZRw-tv025DbK6PO4k3sZhQwWJjZGte7nKuHzJkQ7tR0ub2DOq4Sg6iBDmBFQ00wotCIfcAbgBT4WLWFu8ne9K4GUjz3vtUCALLryWJeIriJnNl7kKxo8BhbEp567PmECfill9RpPkgm3bp6s2GqAtIwWss6hYY02GPm_cssFwLl_fRBzQcFxg30i3oMgg-Xj5flewEC8sdPXdzXg9PJTLmppfKdnYtgPCTR8a2mTgy_B8vXXrkX636qk_FaT9C0QWxMg6fII_5vqRdx65uAVWqc69bm0ikSz_PgnK5flkwLRQr4D5CvZNCw7xngrEBTP42O0mjtbQJZPYzF3__pdpwqli1Ja1WNEC0EZtzi_2xs7rn07qVv2ZeQ0mObp4gs2uyflQZ-6Mv7S2MnJ00Bn7M_kl6S9a1jRHQDnCe61yfgQr8oGvfI7jaiN-8IMphzdkpK4nO4euWk8M5XQFpIorVyLT2RtIUQlA4L6GQBBuixZxI7nt2AA9ZA4J5cTukYGqT908NJ3g8HEpbWvuZ8kFOXAVi8EJqN9OFDXB5qPDfXFZ6lH7-UmYPKLOjrscX9LUSz_Onu65SVJlylHqorkK0mVOQgo7oaM", "p": "00FDBBfSFIbQYJ8yOCJ7c6ZPLmJxQ7_Fch01KdHJvKjKinb5dDtJMxgZzKwPudBajJWE4ucVMuRYRv4QMJWXov6CaLKN-SHkMFIwWMN-UJAVGT7e_iIq1_BrvFvTeFY9zshpuyFiP4lDNzPH1xX2aD0lCt42l-1rfScm1LIO0LYy1Qqma6m-aaKLAcBpr-6SM3A7-YqNVP3enZevPTz6rgZ_boKICVdR-a3vLNb5w1sP_18I3Fcb0vGCsoxuNh46DaDdSs2jkwPmIrra040vstoXHjOLzlubrrH69WqkbNtHf1DRcKgh7fzgHwuzovC6Bn142cdCmr9aLyVgExFUNw", "q": "yhYlTst5WmxYynEtYU9GBqysQnjJSh1gDKocbJv_7AHdfIMnK8tHdqEByj9DPgao76yZt1fGSN9v1B3PhVYYrhdLvtksdYjUgnu0vjtg7kHsDxwY6H4nZykxWr1tjcWHHmcUnlWU_vtkg1pES8_WJ-dtH0IYe0luPRqVqs8YYKL6He-pRbPj4YJJ6KtYgYFpSKbS3hGHDeEo_Bwz9-cP6Q6NxJwgeOZz8BtryHo4gh77RapZcpxH320Fw993xYewpAt_Bi7OqasH8-DwxMSxK-VuAjgfokxZMX2rQXLGO8xVRTVmXGbAK7deWuvlO1qgCHVxZswzI1aNyMjQ4ze_9Q", "qi": "nh4sH934RRsFA_T68m0sas6i9NaRYLOYHiK-Z4QUHxpG4lXVM1Q80srDWTYX_bGCa6R2xLTnYkICN4Y3vnUFxbfD4iBRKGdmepegF7jajbBAqCpCHDRTJUisd6MF--VOy-HPB2uIpDRw2X-g01k-AEqy7sXu1YEfh9_jEBf2JXV86mylJEqWJJT4zEtu18pq1ZV157-dLezHt1IZ9VJJldXgj1ZQza8T-15vQFfiwx1vLKZI3YiRlYVPEhCSfSqFh1C6Im9vQ8R_4kymnzDXJirzZZPJKr0FoFlJEUX8mFMCHrhqi0-OSMrCRxci_40Gtd08qo40iWjid0szYeAjfA" }
pub_keys = { 'enc': {}, 'sig': {} }


def main():
    # Fetch jwks.json, find the encryption and signature public keys then store them.
    url = "https://preprod.signicat.com/oidc/jwks.json"
    r = requests.get(url)
    res = r.json()["keys"]
    for k in res:
        if 'RSA' in k["kty"] and 'enc' in k["use"]:
            pub_keys['enc'] = k
        if 'RSA' in k["kty"] and 'sig' in k["use"]:
            pub_keys['sig'] = k

    # "Packs" some of the keys into JWK classes from the jwcrypto library
    full_key = jwk.JWK()
    full_key.import_key(**jwk_full)
    sigpub_key = jwk.JWK()
    sigpub_key.import_key(**pub_keys['sig'])

    # Prepare and encrypt the payload.
    payload = {
        "ui_locales": "en",
        "scope": "openid profile",
        "acr_values": "urn:signicat:oidc:method:ftn-nordea-auth",
        "response_type": "code",
        "redirect_uri": "https://labs.signicat.com/redirect",
        "state": "ABCDEF0123456789",
        "client_id": "demo-ftnenc",
    }
    enc = encryptRequest(pub_keys['enc'], json.dumps(payload))


    # STEP 1: Generate the "Authorize URL", display it be opened manually in browser.
    url1 = ('https://preprod.signicat.com/oidc/authorize?request={}'.format(enc))
    print("Authorize URL: '{}'".format(url1))
    # User inputs code from authorize response.
    code = input("\nPlease complete the authentication in a browser, then input the code here: ")

    # STEP 2: Call /token end-point as normal (using CODE we got in STEP 1)
    headers = {
        'Authorization': 'Basic ZGVtby1mdG5lbmM6bXFaLV83NS1mMndOc2lRVE9OYjdPbjRhQVo3emMyMThtclJWazFvdWZhOA=='}
    payload = {
        'client_id': 'demo-ftnenc',
        'redirect_uri': 'https://labs.signicat.com/redirect',
        'grant_type': 'authorization_code',
        'code': code
    }
    res1 = requests.post('https://preprod.signicat.com/oidc/token', data=payload, headers=headers).json()
    print("\nGot access token and ID token from /token end-point!\n")
    at = res1['access_token'] # Access token!
    idt = res1['id_token']  # ID token!


    # STEP 3: Process our ID token.
    payload_idtoken = processResponse(idt, full_key, sigpub_key)
    print("\nDecrypting ID token ({} bytes)... Done!".format(len(idt)))
    print("\nSigned token (JWS) - inside the ID token JWE:\n{}".format(payload_idtoken[0]))
    print("\nDecrypted ID token payload:\n{}\n".format(payload_idtoken[1]))

    # STEP 4 (optional): Call /userinfo with access token.
    headers3 = {'Authorization': 'Bearer ' + at}
    res2 = requests.get('https://preprod.signicat.com/oidc/userinfo', headers=headers3).text
    print("\nGot UserInfo token from /userinfo end-point!")


    # STEP 5: Process our UserInfo response.
    payload_idtoken = processResponse(res2, full_key, sigpub_key)
    print("\nDecrypting UserInfo ({} bytes)... Done!".format(len(res2)))
    print("\nSigned token (JWS) - inside the UserInfo JWE:\n{}".format(payload_idtoken[0]))
    print("\nDecrypted UserInfo:\n{}".format(payload_idtoken[1]))

def encryptRequest(jwk_pub, payload):
    """Return a compact serialized JWT, encrypted with jwk_pub, contains the payload specified."""
    public_key = jwk.JWK()
    public_key.import_key(**jwk_pub)
    payload_bytes = payload.encode('utf-8')
    protected_header = {
        "alg": jwk_pub["alg"],
        "enc": "A256CBC-HS512",
        "typ": "JWE",
        "kid": jwk_pub["kid"],
    }
    jwetoken = jwe.JWE(payload_bytes, recipient=public_key, protected=protected_header)
    return jwetoken.serialize(compact=True)


def processResponse(token, enc_key, sig_key):
    """Processes a nested encrypted and signed JWT, returns the payload as a list of two strings."""
    payload = []
    # Decrypt encrypted token (JWE).
    enc = jwe.JWE()
    enc.deserialize(token, key=enc_key)
    payload.append(enc.payload.decode("utf-8"))
    # This again contains a signed token (JWS), so we deserialize it and verify the signature.
    sig = jws.JWS()
    sig.deserialize(payload[0])
    sig.verify(sig_key)
    payload.append(sig.payload.decode("utf-8"))
    return payload

if __name__ == '__main__':
    main()
