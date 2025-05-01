#!/bin/bash

# Import required keys
gpg --import bob_private.key
gpg --import alice_public.asc

# Decrypt and verify
gpg --decrypt signed_message.asc > decrypted_message.txt

echo "Message decrypted and signature verified. Output saved to decrypted_message.txt"
