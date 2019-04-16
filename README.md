# OIDC Full Message-Level Encryption

---

This repository aims to show examples and give some information on how to use "Full Message-Level Encryption" with the Signicat OIDC server.

This includes:

* Encrypting your request to /authorize Signicat OIDC end-point
* Processing encrypted responses from Signicat OIDC end-points

## **authorize-encrypt-examples**

Very simple implementation of how to prepare an encrypted Authorize request, in the following languages:

* C#
* Java
* Python
* node.js

See [./authorize-encrypt-examples/](./authorize-encrypt-examples/) for more information.

## **py-ftn-example**

How to perform an OIDC flow with Full Message-Level Encryption, as specified in the requirements for FTN (Finnish Trust Network).

See [./py-ftn-example/](./py-ftn-example/) for more information.
