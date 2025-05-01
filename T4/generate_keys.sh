#!/bin/bash

# Generate Alice's key
echo "Generating Alice's GPG key..."
gpg --batch --generate-key <<EOF
Key-Type: RSA
Key-Length: 2048
Name-Real: Alice
Name-Email: alice@example.com
Expire-Date: 0
%no-protection
%commit
EOF

# Export Alice's keys
gpg --armor --export alice@example.com > alice_public.asc
gpg --armor --export-secret-keys alice@example.com > alice_private.key

# Generate Bob's key
echo "Generating Bob's GPG key..."
gpg --batch --generate-key <<EOF
Key-Type: RSA
Key-Length: 2048
Name-Real: Bob
Name-Email: bob@example.com
Expire-Date: 0
%no-protection
%commit
EOF

# Export Bob's keys
gpg --armor --export bob@example.com > bob_public.asc
gpg --armor --export-secret-keys bob@example.com > bob_private.key

echo "Key generation complete. Public and private keys exported."
